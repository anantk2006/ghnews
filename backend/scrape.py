 
import requests
from llm_wrapper import LLMWrapper
from firecrawl import FirecrawlApp

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

    def filter_quality(self, links, dates):
        relevant_info = []
        for i in range(len(links)):
            if dates[i] and int(dates[i][2:4])>=24 and int(dates[i][5:7])>=10:
                if self.llm.classify_importance(links[i][0]):
                    relevant_info.append(links[i])
        return relevant_info

    def find_relevant_links(self, package_name):
        # Get news from Bing Search API
        response_web, dates_web = self.search(package_name)
        response_news, dates_news = self.search_news(package_name)
        
        # Only use the good ones that are recent
        relevant_web = self.filter_quality(response_web, dates_web)
        relevant_news = self.filter_quality(response_news, dates_news)
        return relevant_web, relevant_news
    
class Scrape:
    def __init__(self, llm):
        self.llm = llm
        self.app = FirecrawlApp(api_key="fc-571037d21e434541b3747bfdecb42eae")
        self.bing = BingSearch(llm)
    """
    Will return a list of titles, classifications, and markdown content for news and tutorials and maybe papers.
    [(title, classification, markdown_content),....]
    @param query: str
    @return: list
    """
    def get_markdown_content(self, query):
        relevant_web, relevant_news = self.bing.find_relevant_links(query)
        relevant_info = relevant_web + relevant_news
        classifications = [self.llm.classify_type(info[0]) for info in relevant_info]
    

if __name__ == "__main__":
    llm = LLMWrapper()
    bing = BingSearch(llm)
    bing.find_relevant_links("machine learning")