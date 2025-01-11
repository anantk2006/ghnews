 
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
        self.news_endpoint = f"https://www.google.com/search?sca_esv=a5656b49a3739dcb&rlz=1C1ONGR_enUS977US977&sxsrf=ADLYWILKxjgubkuPUCIn18j-c9kzJ2CpDQ:1736549267956&tbm=nws&source=lnms&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWxyMMuf0D-HOMEpzq2zertb7e7Ciu-gKKGrwTISbKLfFIYx49Dyz2pn9q3XAGT3GlZzYbV_yo73lZ_m2LipeQYsyJUKGJZPL_qptJKAatZvwmB_4U1rSVeZB6yCZoBjje8QMPLrSzGTZfEb08Se95XUxV45ehpxMas3jQD98fxKWLpOpC98hL9Z6jJvLxnZvrXgvKrQ&sa=X&sqi=2&ved=2ahUKEwjlnIGSnuyKAxVlRjABHR-8G2YQ0pQJegQIEhAB&biw=1536&bih=730&dpr=1.25&q=after:{week_ago_year}-{week_ago_month}-{week_ago_day}+"
        self.llm = llm

    def search(self, queries):
        # Add your Bing Search V7 subscription key and endpoint to your environment variables.
        # Construct a request
        # Call the API
        print("fuck you", flush=True)
        query_to_links = []
        queries = ["+".join(query.split(" ")) for query in queries]
        links = [self.endpoint + query for query in queries]
        loop = asyncio.get_event_loop()
        news_content = loop.run_until_complete(self.fetch_all())
        
        for r in res:

        # for query in queries:
        #     res = 
        #     soup = BeautifulSoup(res.text, 'html.parser')
        #     links = soup.find_all('a')
        #     domains = set()
        #     fins = []
        #     titles = []
        #     for link in links:
        #         href = link.get('href')
        #         if "google" not in href and "https" in href:
        #             bound = href.index("//") + 2
        #             up = href[bound:].index("/")
        #             domain = href[bound:bound + up]
        #             if domain not in domains:
        #                 fins.append(link.get('href'))
        #                 domains.add(domain)
        #                 title = link.text
        #                 titles.append(title)

    def search_news(self, queries):
        # Add your Bing Search V7 subscription key and endpoint to your environment variables.
        # Construct a request
        # Call the API
        try:
            response = requests.get(self.news_endpoint, headers=headers, params=params)
            response.raise_for_status()
            response = response.json()
        except Exception as ex:
            raise ex
        

    def filter_quality(self, links, dates, news=False):
        relevant_info = []
        yr = 25 if news else 24
        mo = 1 if news else 9
        for i in range(len(links)):
            if dates[i] and int(dates[i][2:4])>=yr and int(dates[i][5:7])>=mo:
                if self.llm.classify_importance(links[i][0]):
                    relevant_info.append(links[i])
        return relevant_info
    
    def find_relevant_links_web(self, topic):
        # Get news from Bing Search API
        response_web, dates_web = self.search(topic)
        # Only use the good ones that are recent
        relevant_web = self.filter_quality(response_web, dates_web)
        return relevant_web

    def find_relevant_links_news(self, topic):
        # Get news from Bing Search API
        response_news, dates_news = self.search_news(topic)
        
        # Only use the good ones that are recent
        relevant_news = self.filter_quality(response_news, dates_news, news=True)
        return relevant_news
    
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
        for id in ids:
            response = requests.get(self.ARXIV_PAPER_URL + id)
            soup = BeautifulSoup(response.text, 'html.parser')
            abstract = soup.find('blockquote', {'class': 'abstract mathjax'}).text
            title = soup.find('h1', {'class': 'title mathjax'}).text
            if self.llm.classify_importance(title):
                abstracts.append((title, abstract))
        return abstracts     
        
class Scrape:
    def __init__(self, llm):
        self.llm = llm
        self.bing = BingSearch(llm)
        self.arxiv = ArxivSearch(llm)
        self.embed = ArcticEmbed()
    """
    Will return a list of titles, classifications, and markdown content for news and tutorials and maybe papers.
    [(title, classification, markdown_content),....]
    @param query: str
    @return: list
    """

    
    def get_markdown_content(self, topics, type):
        topic_to_text = {}
        for topic in topics:
            topic_to_text[topic] = []     
            if type == "news":       
                news_links = self.bing.find_relevant_links_news(topic)
            elif type == "web":
                news_links = self.bing.find_relevant_links_web(topic + "tutorial")
            else:
                raise ValueError("Type must be 'news' or 'web'")
            news_links = [l[1] for l in news_links]
            loop = asyncio.get_event_loop()
            news_content = loop.run_until_complete(self.fetch_all(news_links))
            topic_to_text[topic] = news_content
        return topic_to_text

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
    asyncio.run(ggl.search(["software engineering", "machine learning"]))
