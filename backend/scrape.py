 
from bs4 import BeautifulSoup
import requests
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
        images = [r['image']['thumbnail']['contentUrl'] 
                  if 'image' in r 
                  and 'thumbnail' in r['image'] 
                  and 'contentUrl' in r['image']['thumbnail'] else None 
                  for r in response['value']
                  ]
        for i in range(len(response['value'])):
            links.append((response['value'][i]['name'], (response['value'][i]['url'], images[i])))       
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
            fin = []
            for i, link in enumerate(links):
                fin.append([link[0], None, link[1], links[:i] + links[i+1:]])
            for f in fin:
                g = [{"title": link[0], "link": link[1]} for link in f[-1]]
                f[-1] = g
                
            topic_to_links[topic] = fin
        return topic_to_links


    
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
        urls = self.get_arxiv_urls()[:10] # TODO: Change to 300
        
        content = [requests.get(url).text for url in urls]
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
            abstract = list(abstract) + [{"link": abstracts[int(j)][2], "title": abstracts[int(j)][0]}
                                          for j in cross_likes[i][1:]]
            if topic in topic_to_text:
                topic_to_text[topic].append(abstract)
            else:
                topic_to_text[topic] = [abstract]
        return topic_to_text





    
