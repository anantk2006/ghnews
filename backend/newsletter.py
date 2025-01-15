import sqlite3
from topics import ArcticEmbed
from llm_wrapper import LLMWrapper
from scrape import Scrape

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown
import schedule
import time

top_k_topics = 4

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
        user_emails[user_id] = [content[topic] for topic, _ in top_k]
    return user_emails

def run_arxiv():
    id_to_email, user_to_topic_to_skill = retrieve_user_info()   
    llm = LLMWrapper()
    scrape = Scrape(llm)
    arxiv_abstracts = scrape.get_arxiv_content()
    user_emails = match_content(user_to_topic_to_skill, arxiv_abstracts)

def run_web():
    run_search(search_type="web")

def run_news():
    run_search(search_type="news")

def run_search(search_type):
    id_to_email, user_to_topic_to_skill = retrieve_user_info()
    llm = LLMWrapper()
    scrape = Scrape(llm)
    topics = scrape.embed.topics
    topic_to_links = scrape.get_links_from_db(search_type, topics)[0]
    topic_to_content = scrape.markdown_helper(topic_to_links, search_type)
    user_emails = match_content(user_to_topic_to_skill, topic_to_content)
    print(user_emails)







def main():
    # schedule.every(1).day.do(run_arxiv)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(10)  
    # run_arxiv()
    run_web()
    
if __name__ == "__main__":
    main()