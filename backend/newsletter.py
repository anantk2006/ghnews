import sqlite3
from scrape import find_relevant_info
from firecrawl import FirecrawlApp
from llm_wrapper import LLMWrapper

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown

def get_topics_from_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT topic FROM topics")
    topics = cursor.fetchall()
    conn.close()
    
    return list(set([topic[0] for topic in topics]))

def get_text_for_all_topics(llm):
    topics = get_topics_from_db()
    app = FirecrawlApp(api_key="fc-571037d21e434541b3747bfdecb42eae")
    links = []
    for topic in topics[:1]:
        relevant_info = find_relevant_info(topic, " news")
        dates_of_pub = ["9"*20 if 'datePublished' not in r else r['datePublished'] for r in relevant_info['webPages']['value']]
        recent = {i for i, d in enumerate(dates_of_pub) if d and int(d[2:4])>=24 and int(d[5:7])>=10}
        relevant_info = [i for i in relevant_info['webPages']['value'] if llm.classify_importance(i['name'])]
        links.extend([(topic, r['url']) for i, r in enumerate(relevant_info) if i in recent])
    batch_scrape_result = app.batch_scrape_urls([l[1] for l in links][:3], {'formats': ['markdown']})
    topic_to_text = {topic: [] for topic in topics}
    for i, r in enumerate(batch_scrape_result['data']):
        topic_to_text[links[i][0]].append(r['markdown'])
    return topic_to_text

def send_email(email_address, subject, markdown_text):
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_text)
    
    # Create message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'your_email@example.com'
    msg['To'] = email_address
    
    # Record the MIME types of both parts - text/plain and text/html
    part1 = MIMEText(markdown_text, 'plain')
    part2 = MIMEText(html_content, 'html')
    
    # Attach parts into message container
    msg.attach(part1)
    msg.attach(part2)
    
    # Send the message via local SMTP server
    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login('your_email@example.com', 'your_password')
        server.sendmail('your_email@example.com', email_address, msg.as_string())
    
def main():
    llm = LLMWrapper()
    topic_to_text = get_text_for_all_topics(llm)  
    articles = llm.make_articles(topic_to_text)
    print(articles)
    
if __name__ == "__main__":
    main()