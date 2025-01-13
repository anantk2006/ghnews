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

def run_arxiv():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT user_id, user_email FROM users
    ''')
    emails = cursor.fetchall()
    emails = [email[0] for email in emails]
    ids = [email[1] for email in emails]
    id_to_email = dict(zip(ids, emails))
    cursor.execute('''
                   SELECT user_id, topic, skill_level FROM user_skills
                   ''')
    user_skills = cursor.fetchall()
    user_to_topic_to_skill = {}
    user_to_skill_sort = {}
    for user_id, topic, skill in user_skills:
        if user_id not in user_to_topic_to_skill:
            user_to_topic_to_skill[user_id] = {}
        user_to_topic_to_skill[user_id][topic] = skill
        if user_id not in user_to_skill_sort:
            user_to_skill_sort[user_id] = []
        user_to_skill_sort[user_id].append((skill, topic))
    for user_id, skill_topic in user_to_skill_sort.items():
        skill_topic.sort(reverse=True)
        user_to_skill_sort[user_id] = set(skill_topic[:50])

    llm = LLMWrapper()
    scrape = Scrape(llm)
    arxiv_abstracts = scrape.get_arxiv_abstracts()
    user_emails = {}
    for topic, abstract in arxiv_abstracts:
        for user_id, topic_to_skill in user_to_topic_to_skill.items():
            if topic in topic_to_skill:
                if topic in user_to_skill_sort[user_id]:
                    if user_id not in emails:
                        user_emails[user_id] = []
                    user_emails[user_id].append((topic, abstract))
    print(user_emails)
    

        

    conn.close()


def main():
    schedule.every(1).day.do(run_arxiv)

    while True:
        schedule.run_pending()
        time.sleep(10)  
    
if __name__ == "__main__":
    main()