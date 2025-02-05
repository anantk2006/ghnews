 
from bs4 import BeautifulSoup
import requests
import asyncio
import aiohttp
import sqlite3 
from gnews import GNews

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

class GoogleNews:
    def __init__(self, llm):
        self.llm = llm
        self.gnews = GNews()
        self.gnews.period = "7d"
    def search(self, topics):
        topic_to_links = {}
        for topic in topics:
            links = [(g['title'], g['url']) for g in self.gnews.get_news(topic)][:5]
            topic_to_links[topic] = [link for link in links if self.llm.classify_importance_news(link[0])]
        return topic_to_links

class BingSearch:
    def __init__(self, llm):
        self.subscription_key = "eda35cadd4834ce997da0375b171e61c"
        self.endpoint = "https://api.bing.microsoft.com/v7.0/search/"
        self.news_endpoint = "https://api.bing.microsoft.com/v7.0/news/search"
        self.llm = llm


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
                if self.llm.classify_importance_news(links[i][0]):
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
    
    def search(self, topics):
        topic_to_links = {}
        for topic in topics:
            links = self.find_relevant_links_news(topic)
            topic_to_links[topic] = links
        return topic_to_links

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
        urls = self.get_arxiv_urls()[:10]
        loop = asyncio.get_event_loop()
        content = loop.run_until_complete(fetch_all(urls, format="text"))
        for i, response in enumerate(content):
            soup = BeautifulSoup(response, 'html.parser')
            abstract = soup.find('blockquote', {'class': 'abstract mathjax'}).text
            title = soup.find('h1', {'class': 'title mathjax'}).text
            if self.llm.classify_importance_research(title):
                abstracts.append((title, abstract, urls[i]))
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
    
    def markdown_helper(self, links, search_type):
        ret = []
        for link in links:
            text = requests.get("https://r.jina.ai/" + link).text
            if "Slow down, turbo".lower() in text.lower():
                ret.append('None')
                time.sleep(60)
            else:
                cleaned = re.sub(r'\(.*?\)', '', text)
                cleaned = re.sub(r'\[.*?\]', '', cleaned)
                ret.append(cleaned)
        return ret                

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
        
        cross_sim = final_embeddings @ final_embeddings.T
        cross_likes = torch.topk(cross_sim, 5, dim=1)[1]
        # Get the proper dictionary
        topic_to_text = {}
        for i, topic_idx in enumerate(user_topics):
            topic = self.embed.paper_topics[int(topic_idx)]
            abstract = abstracts[i]
            abstract = list(abstract) + [abstracts[int(j)][2] for j in cross_likes[i][1:]]
            if topic in topic_to_text:
                topic_to_text[topic].append(abstract)
            else:
                topic_to_text[topic] = [abstract]
        print(topic_to_text)
        return topic_to_text


if __name__ == "__main__":
    embed = ArcticEmbed()
    llm = LLMWrapper()
    ggl = GoogleNews(llm)
    print(ggl.search(embed.news_topics))


    
