import sqlite3
from topics import ArcticEmbed
from llm_wrapper import LLMWrapper
from scrape import Scrape

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown

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

def send_arxiv_content(llm, embedder, scrape):
    abstracts = scrape.get_arxiv_abstracts()
    for abstract in abstracts:
        title, abstract = abstract


    
def main():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT user_email
    FROM users
    ''')
    users = cursor.fetchall()
    conn.close()
    
    llm = LLMWrapper()
    scrape = Scrape(llm)
    embed = ArcticEmbed()
    
    
        
    
    
    
if __name__ == "__main__":
    main()