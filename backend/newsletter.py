import sqlite3
from topics import ArcticEmbed
from llm_wrapper import LLMWrapper
from scrape import Scrape

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown
import schedule
import datetime, time
import random
from scrape import GoogleNews, BingSearch

top_k_topics = 10
llm = LLMWrapper()
scrape = Scrape(llm)
google_news = GoogleNews(llm)
bing_news = BingSearch(llm)

def send_email(email_address, subject, markdown_text):
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_text)
    
    # Create message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'anantk2006@gmail.com'
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
        server.login('anantk2006@gmail.com', 'anantk2006')
        server.sendmail("anantk2006@gmail.com", email_address, msg.as_string())

def retrieve_user_info():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT user_id, user_email FROM users
    ''')
   
    info = cursor.fetchall()
    emails = [email[0] for email in info if email]
    ids = [email[1] for email in info if email]
    
    id_to_email = dict(zip(ids, emails))
    cursor.execute('''
                   SELECT user_id, topic, skill_level FROM user_skills
                   ''')
    user_skills = cursor.fetchall()
    user_to_topic_to_skill = {}
    
    for user_id, topic, skill in user_skills:
        if user_id not in user_to_topic_to_skill:
            user_to_topic_to_skill[user_id] = {}
        user_to_topic_to_skill[user_id][topic] = skill
    return id_to_email, user_to_topic_to_skill

def match_content(user_to_topic_to_skill, content):
    user_emails = {}
    for user_id in user_to_topic_to_skill:
        todays_topics = list(content.keys())
        top_k = [(topic, user_to_topic_to_skill[user_id][topic]) for topic in todays_topics[:top_k_topics]]
        for topic in todays_topics[top_k_topics:]:
            if topic in user_to_topic_to_skill[user_id]:
                if user_to_topic_to_skill[user_id][topic] > top_k[-1][1]:
                    i = top_k_topics - 1
                    while i >= 0 and user_to_topic_to_skill[user_id][topic] > top_k[i][1]:
                        if i<=top_k_topics-2: top_k[i+1] = top_k[i]
                        i -= 1
                    top_k[i+1] = (topic, user_to_topic_to_skill[user_id][topic])
        user_emails[user_id] = random.sample([content[topic] for topic, _ in top_k], 5)
    return user_emails

def run_arxiv():
    id_to_email, user_to_topic_to_skill = retrieve_user_info()   
    llm = LLMWrapper()
    scrape = Scrape(llm)
    arxiv_abstracts = scrape.get_arxiv_content()
    user_emails = match_content(user_to_topic_to_skill, arxiv_abstracts)
    user_emails = text_to_articles(user_emails)
    make_and_send_emails(user_emails, id_to_email, search_type="arxiv")

def links_to_articles(user_emails):
    links_to_user = {}
    for user_id, emails in user_emails.items():
        for email in emails:
            for link_holder in email:
                link = link_holder[1]
                if link not in links_to_user:
                    links_to_user[link] = []
                else: links_to_user[link].append(user_id)
    links = list(links_to_user.keys())
    
    scraped = scrape.markdown_helper(links, "news")
    articles = llm.make_articles(scraped)
    print(articles)
    ret = {}
    for link, text in zip(links, articles):
        for user_id in links_to_user[link]:
            if user_id not in ret:
                ret[user_id] = [text]
            else: ret[user_id].append(text)
    
    return ret

    





def run_news():
    
    id_to_email, user_to_topic_to_skill = retrieve_user_info()
    topics = random.sample(scrape.embed.topics, 6)
    topic_to_links = bing_news.search(topics)
    user_emails = match_content(user_to_topic_to_skill, topic_to_links)
    user_emails = links_to_articles(user_emails)
    print(user_emails)
    exit()
    make_and_send_emails(user_emails, id_to_email, search_type="news")
    
def run_search(scrape, llm, search_type):
    
    if datetime.datetime.now() > scrape.last_scraped_news + datetime.timedelta(days=1):
        scrape.last_scraped_news = datetime.datetime.now()
        ttl = scrape.ggl.find_relevant_links(topics, search_type)
        scrape.add_links_to_db(ttl, search_type)
    if datetime.datetime.now() > scrape.last_scraped_tutorials + datetime.timedelta(days=90):
        scrape.last_scraped_tutorials = datetime.datetime.now()
        ttl = scrape.ggl.find_relevant_links(topics, search_type)
        scrape.add_links_to_db(ttl, search_type)
    id_to_email, user_to_topic_to_skill = retrieve_user_info()
    topics = scrape.embed.topics
    topic_to_links, count = scrape.get_links_from_db(search_type, topics)
    print(topic_to_links)
    if count < 200:
        ttl = scrape.ggl.find_relevant_links(topics[:5], search_type)
        print(ttl)
        scrape.add_links_to_db(ttl, search_type)
    topic_to_content = scrape.markdown_helper(topic_to_links, search_type)
    user_emails = match_content(user_to_topic_to_skill, topic_to_content)
    print(user_emails)

def make_and_send_emails(user_emails, id_to_email, search_type = "news"):
    type_str = 'Curated News For You' if search_type == 'news' else 'Recent Paper Abstracts For You'
    user_emails = llm.make_articles(user_emails)
    for user_id, emails in user_emails.items():
        email_address = id_to_email[user_id]
        for email in emails:
            send_email(email_address, type_str, email)





def main():
    # schedule.every(1).day.do(run_arxiv)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(10)  
    # run_arxiv()
    run_news()
    
if __name__ == "__main__":
    main()