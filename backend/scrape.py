 
from bs4 import BeautifulSoup
import requests
import asyncio
import aiohttp
import sqlite3 

from llm_wrapper import LLMWrapper

from topics import ArcticEmbed
import torch

import datetime
import re
import json
import time


"""
Helpers for async fetching of web content
"""
async def fetch_text(session, url):
    
    async with session.get(url, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}) as response:
        return await response.text()
    
async def fetch_json(session, url):
    async with session.get(url, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}) as response:
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

class GoogleSearchAPI:
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

    def search(self, searches, search_type = "web"):
        # batch requests to google search for all queries
        def get_links_rate_limit(batched_links):
            content = []
            for batch in batched_links:
                print(batch)
                content.extend(asyncio.get_event_loop().run_until_complete(fetch_all(batch, format="text")))
                time.sleep(1)
            return content
        query_to_links = {}
        ext = "+news" if search_type == "news" else "+tutorial"
        queries = ["+".join(query.split(" ")) + ext for query in searches]
        links = [(self.endpoint if search_type == "web" else self.news_endpoint) + query for query in queries]
        batched_links = [links[i: i + 1] for i in range(0, len(links), 1)]
        content = get_links_rate_limit(batched_links)
        # Analyze one by one and map to query
        for query, html in zip(searches, content):
            soup = BeautifulSoup(html, 'html.parser')
            to_scrape = soup.find_all('a')
            domains = set()            
            ret = []
            for link in to_scrape:
                href = link.get('href')
                if "google" not in href and "https://" in href:
                    print(href)
                    bound = href.index("//") + 2
                    up = href[bound:].index("/")
                    domain = href[bound:bound + up]
                    # google gives many different links for a single thing
                    if domain not in domains:
                        domains.add(domain)
                        ret.append((link.text, href[7:href.index("&sa=")]))
            query_to_links[query] = ret            
        return query_to_links        

    def filter_quality(self, links, search_type = "web"):
        relevant_info = []
        classifier = self.llm.classify_importance_news if search_type == "news" else self.llm.classify_importance_web
        for i in range(len(links)):            
            if classifier(links[i][0]):
                relevant_info.append(links[i])
        return relevant_info
    
    def find_relevant_links(self, topics, search_type = "web"):
        # Get news from google search
        response_web = self.search(topics, search_type=search_type)
        # Only use the good ones
        for query in response_web:
            response_web[query] = self.filter_quality(response_web[query], search_type=search_type)    
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
    
    def get_arxiv_urls(self):
        ids = self.get_arxiv_ids()
        return [self.ARXIV_PAPER_URL + id for id in ids]

    def get_arxiv_abstracts(self):
        abstracts = []
        urls = self.get_arxiv_urls()
        loop = asyncio.get_event_loop()
        content = loop.run_until_complete(fetch_all(urls, format="text"))
        for response in content:
            soup = BeautifulSoup(response, 'html.parser')
            abstract = soup.find('blockquote', {'class': 'abstract mathjax'}).text
            title = soup.find('h1', {'class': 'title mathjax'}).text
            if self.llm.classify_importance_research(title):
                abstracts.append((title, abstract))
        return abstracts     
        
class Scrape:
    def __init__(self, llm):
        self.llm = llm
        self.ggl = GoogleSearch(llm)
        self.arxiv = ArxivSearch(llm)
        self.embed = ArcticEmbed()
        self.last_scraped_news = datetime.datetime.now()
        self.last_scraped_tutorials = datetime.datetime.now()
    
    def add_links_to_db(self, topic_to_links, search_type):
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        for topic, links in topic_to_links.items():
            for link in links:
                cursor.execute('''
                INSERT INTO links (topic, search_type, link)
                VALUES (?, ?, ?)
                ''', (topic, search_type, link))
        db.commit()
        db.close()
    
    def get_links_from_db(self, search_type, topics):
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        topic_to_links = {}
        count = 0
        for topic in topics:
            cursor.execute('''
                SELECT link FROM links WHERE topic = ? AND search_type = ? LIMIT 200
                ''', (topic, search_type))
            links = cursor.fetchall()
            for link in links:
                cursor.execute('''
                    DELETE FROM links WHERE link = ?
                    ''', (link[0],))            
            topic_to_links[topic] = [link[0] for link in links]
            count += len(links)
        db.commit()
        db.close()        
        return topic_to_links, count
    
    def markdown_helper(self, topic_to_links, search_type):
        for topic, links in topic_to_links.items():
            # Construct jina links and scrape for markdown content
            jina_links = ["https://r.jina.ai/" + link[1] for link in links]
            content = asyncio.get_event_loop().run_until_complete(fetch_all(jina_links, format="text"))
            # Prevent rate limiting
            init_len = len(content)
            content = [c for c in content if "Slow down, turbo!" not in c]
            if len(content) != init_len:
                print("Rate limited, sleeping for 60 seconds")
                time.sleep(60)
            cleaned_content = []
            if content:
                for c in content:
                    cleaned = re.sub(r'\(.*?\)', '', c)
                    cleaned = re.sub(r'\[.*?\]', '', cleaned)
                cleaned_content.append(cleaned)
                topic_to_links[topic] = cleaned_content
        return topic_to_links

    def get_markdown_content(self):
        # Get news and web content
        news_t2t = self.markdown_helper(self.embed.news_topics, "news")
        web_t2t = self.markdown_helper(self.embed.tutorial_topics, "web")
        return news_t2t, web_t2t              
        
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
    print(ggl.find_relevant_links(["python", "java", "c++"], search_type="web"))
    
