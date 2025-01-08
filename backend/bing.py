 
from pprint import pprint
import requests


BING_SEARCH_V7_SUBSCRIPTION_KEY = "eda35cadd4834ce997da0375b171e61c"
BING_SEARCH_V7_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search/"
BING_SEARCH_V7_NEWS_ENDPOINT = "https://api.bing.microsoft.com/v7.0/news/search"

def search(query):
    # Add your Bing Search V7 subscription key and endpoint to your environment variables.
    subscription_key = BING_SEARCH_V7_SUBSCRIPTION_KEY
    endpoint = BING_SEARCH_V7_ENDPOINT

    # Construct a request
    mkt = 'en-US'
    params = { 'q': query, 'mkt': mkt }
    headers = { 'Ocp-Apim-Subscription-Key': subscription_key }

    # Call the API
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
    except Exception as ex:
        raise ex
    return response.json()

def find_relevant_info(package_name, aux_info):
    response = search(package_name + aux_info)
    return response

if __name__ == "__main__":
    pprint(find_relevant_info("federated learning", " latest trends"))