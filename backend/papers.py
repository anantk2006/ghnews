"""
Arxiv paper scraper
"""
cs_num = 2248

import requests
from bs4 import BeautifulSoup
import pandas as pd

ARXIV_BASE_URL = "https://arxiv.org/list/cs/recent?skip=0&show=2000"

ARXIV_PAPER_URL = "https://arxiv.org/abs/"

  
def get_arxiv_ids():
    response = requests.get(ARXIV_BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    papers = soup.find_all('a', {'title': 'Download PDF'})
    ids = []
    for paper in papers:
        ids.append(paper['href'].split('/')[-1])
    return ids

def get_arxiv_abstracts():
    ids = get_arxiv_ids()
    for id in ids:
        response = requests.get(ARXIV_PAPER_URL + id)
        soup = BeautifulSoup(response.text, 'html.parser')
        abstract = soup.find('blockquote', {'class': 'abstract mathjax'}).text
        title = soup.find('h1', {'class': 'title mathjax'}).text
        print(abstract)

    
        

get_arxiv_abstracts()



