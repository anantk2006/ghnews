 
import requests
from llm_wrapper import LLMWrapper


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


    def find_relevant_links(self, package_name):
        response = self.search(package_name)
        response_news = self.search_news(package_name)
        print(response_news)
        print(response)
        # dates_of_pub = ["9"*20 if 'datePublished' not in r else r['datePublished'] for r in relevant_info['webPages']['value']]
        # recent = {i for i, d in enumerate(dates_of_pub) if d and int(d[2:4])>=24 and int(d[5:7])>=10}
        # relevant_info = [i for i in relevant_info['webPages']['value'] if llm.classify_importance(i['name'])]

        # for i in range(len(response['webPages']['value'])):
        #     links.append((response['webPages']['value'][i]['name'], response['webPages']['value'][i]['url']))
        # return response

if __name__ == "__main__":
    llm = LLMWrapper()
    bing = BingSearch(llm)
    bing.find_relevant_links("machine learning")