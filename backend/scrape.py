 
import requests
from llm_wrapper import LLMWrapper
from firecrawl import FirecrawlApp
from bs4 import BeautifulSoup
from topics import ArcticEmbed

import torch
import asyncio
import aiohttp
import datetime, time

"""
Helpers for async fetching of web content
"""
async def fetch_text(session, url):
    async with session.get(url) as response:
        return await response.text()
    
async def fetch_json(session, url):
    async with session.get(url) as response:
        return await response.json()

async def fetch_all(urls, format = "json"):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            if format == "json":
                tasks.append(fetch_json(session, url))
            elif format == "text":
                tasks.append(fetch_text(session, url))
            else:
                raise ValueError("Format must be 'json' or 'text'")
        return await asyncio.gather(*tasks)


class GoogleSearch:
    def __init__(self, llm):
        week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        week_ago_day = week_ago.day
        week_ago_month = week_ago.month
        week_ago_year = week_ago.year
        two_months_ago = datetime.datetime.now() - datetime.timedelta(days=60)
        two_months_ago_day = two_months_ago.day
        two_months_ago_month = two_months_ago.month
        two_months_ago_year = two_months_ago.year

        self.endpoint = f"https://www.google.com/search?rlz=1C1ONGR_enUS977US977&q=after:{two_months_ago_year}-{two_months_ago_month}-{two_months_ago_month}+"
        self.news_endpoint = f"https://www.google.com/search?sca_esv=a5656b49a3739dcb&rlz=1C1ONGR_enUS977US977&sxsrf=ADLYWILKxjgubkuPUCIn18j-c9kzJ2CpDQ:1736549267956&tbm=nws&source=lnms&q=after:{week_ago_year}-{week_ago_month}-{week_ago_day}+"
        self.llm = llm

    def search(self, queries, search_type = "web"):
        # batch requests to google search for all queries
        query_to_links = {}
        queries = ["+".join(query.split(" ")) for query in queries]
        links = [(self.endpoint if search_type == "web" else self.news_endpoint) + query for query in queries]
        loop = asyncio.get_event_loop()
        content = loop.run_until_complete(fetch_all(links, format="text"))
        # Analyze one by one and map to query
        for query, html in zip(queries, content):
            soup = BeautifulSoup(html, 'html.parser')
            to_scrape = soup.find_all('a')
            domains = set()            
            ret = []
            for link in to_scrape:
                href = link.get('href')
                if "google" not in href and "https" in href:
                    bound = href.index("//") + 2
                    up = href[bound:].index("/")
                    domain = href[bound:bound + up]
                    # google gives many different links for a single thing
                    if domain not in domains:
                        domains.add(domain)
                        ret.append((link.text, href[7:href.index("&sa=")]))
            query_to_links[query] = ret            
        return query_to_links        

    def filter_quality(self, links):
        relevant_info = []
        for i in range(len(links)):            
            if self.llm.classify_importance(links[i][0]):
                relevant_info.append(links[i])
        return relevant_info
    
    def find_relevant_links(self, topics, search_type = "web"):
        # Get news from google search
        if search_type == "news":
            queries = [topic + "news" for topic in topics]
        else:
            queries = [topic + "tutorial" for topic in topics]
        response_web = self.search(queries, search_type="web")
        # Only use the good ones
        for query in response_web:
            response_web[query] = self.filter_quality(response_web[query])    
        return response_web
    
class ArxivSearch:
    def __init__(self, llm):
        self.ARXIV_BASE_URL = "https://arxiv.org/list/cs/recent?skip=0&show=2000"
        self.ARXIV_PAPER_URL = "https://arxiv.org/abs/" 
        self.llm = llm 

    def get_arxiv_ids(self):
        response = requests.get(self.ARXIV_BASE_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        papers = soup.find_all('a', {'title': 'Download PDF'})
        ids = []
        for paper in papers[:300]:
            ids.append(paper['href'].split('/')[-1])
        return ids

    def get_arxiv_abstracts(self):
        abstracts = []
        ids = self.get_arxiv_ids()
        urls = [self.ARXIV_PAPER_URL + id for id in ids]
        loop = asyncio.get_event_loop()
        content = loop.run_until_complete(fetch_all(urls, format="text"))
        for response in content:
            soup = BeautifulSoup(response.text, 'html.parser')
            abstract = soup.find('blockquote', {'class': 'abstract mathjax'}).text
            title = soup.find('h1', {'class': 'title mathjax'}).text
            if self.llm.classify_importance(title):
                abstracts.append((title, abstract))
        return abstracts     
        
class Scrape:
    def __init__(self, llm):
        self.llm = llm
        self.ggl = GoogleSearch(llm)
        self.arxiv = ArxivSearch(llm)
        self.embed = ArcticEmbed()
    """
    Will return a list of titles, classifications, and markdown content for news and tutorials and maybe papers.
    [(title, classification, markdown_content),....]
    @param query: str
    @return: list
    """

    
    # def get_markdown_content(self, topics, search_type):
    #     query_to_links = self.ggl.find_relevant_links(topics, search_type=search_type)
    #     loop = asyncio.get_event_loop()
    #     news_content = loop.run_until_complete(self.fetch_all(news_links))
            

    def get_arxiv_content(self):
        # Extract and format abstracts
        abstracts = self.arxiv.get_arxiv_abstracts()
        titles = [a[0] for a in abstracts]
        batched_titles = [titles[i:i + 250] for i in range(0, len(titles), 250)]
        all_embeddings = []
        # Embed abstracts and discover topics
        for batch in batched_titles:
            embeddings = self.embed.get_embedding(batch)
            all_embeddings.append(embeddings)
        final_embeddings = torch.cat(all_embeddings, dim=0)
        likes = final_embeddings @ self.embed.paper_embeds.T
        user_topics = torch.argmax(likes, dim=1)
        # Get the proper dictionary
        topic_to_text = {}
        for i, topic_idx in enumerate(user_topics):
            topic = self.embed.paper_topics[int(topic_idx)]
            if topic in topic_to_text:
                topic_to_text[topic].append(abstracts[i][1])
            else:
                topic_to_text[topic] = [abstracts[i][1]]
        return topic_to_text


if __name__ == "__main__":
    llm = LLMWrapper()
    ggl = GoogleSearch(llm)
    print(ggl.find_relevant_links(["software engineering ", "machine learning "], search_type="news"))
