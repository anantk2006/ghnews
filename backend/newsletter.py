import sqlite3
from scrape import find_relevant_info
from firecrawl import FirecrawlApp
from llm_wrapper import LLMWrapper

def get_topics_from_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT topic FROM topics")
    topics = cursor.fetchall()
    conn.close()
    
    return list(set([topic[0] for topic in topics]))

def main():
    topics = get_topics_from_db()
    app = FirecrawlApp(api_key="fc-571037d21e434541b3747bfdecb42eae")
    llm = LLMWrapper()
    links = []
    for topic in topics[:10]:
        relevant_info = find_relevant_info(topic, " news")
        relevant_info = [i for i in relevant_info['webPages']['value'] if LLMWrapper.classify_importance(i['name'])]
        links.extend([r['url'] for r in relevant_info['webPages']['value']])
    batch_scrape_result = app.batch_scrape_urls(links[:10], {'formats': ['markdown']})
    print(batch_scrape_result)
    


if __name__ == "__main__":
    main()