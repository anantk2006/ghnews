 
import requests
from llm_wrapper import LLMWrapper
from firecrawl import FirecrawlApp
from bs4 import BeautifulSoup
from topics import ArcticEmbed

import torch
import asyncio
import aiohttp

"""
Helpers for async fetching of web content
"""
async def fetch(self, session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_all(self, urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(self.fetch(session, url))
        return await asyncio.gather(*tasks)


class BingSearch:
    def __init__(self, llm):
        self.subscription_key = "eda35cadd4834ce997da0375b171e61c"
        self.endpoint = "https://api.bing.microsoft.com/v7.0/search/"
        self.news_endpoint = "https://api.bing.microsoft.com/v7.0/news/search"
        self.llm = llm

    def search(self, query):
        # Add your Bing Search V7 subscription key and endpoint to your environment variables.
        # Construct a request
        mkt = 'en-US'
        params = { 'q': query, 'mkt': mkt }
        headers = { 'Ocp-Apim-Subscription-Key': self.subscription_key }

        # Call the API
        try:
            response = requests.get(self.endpoint, headers=headers, params=params)
            response.raise_for_status()
            response = response.json()
        except Exception as ex:
            raise ex
        links = []
        dates = [False if 'datePublished' not in r else r['datePublished'] for r in response['webPages']['value']]
        for i in range(len(response['webPages']['value'])):
            links.append((response['webPages']['value'][i]['name'], response['webPages']['value'][i]['url']))
        return links, dates

    def search_news(self, query):
        # Add your Bing Search V7 subscription key and endpoint to your environment variables.
        # Construct a request
        mkt = 'en-US'
        params = { 'q': query, 'mkt': mkt }
        headers = { 'Ocp-Apim-Subscription-Key': self.subscription_key }

        # Call the API
        try:
            response = requests.get(self.news_endpoint, headers=headers, params=params)
            response.raise_for_status()
            response = response.json()
        except Exception as ex:
            raise ex
        links = []
        dates = [False if 'datePublished' not in r else r['datePublished'] for r in response['value']]
        for i in range(len(response['value'])):
            links.append((response['value'][i]['name'], response['value'][i]['url']))
        return links, dates

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
    bing = BingSearch(llm)
    bing.find_relevant_links("machine learning")