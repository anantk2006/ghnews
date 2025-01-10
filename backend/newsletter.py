import sqlite3
from firecrawl import FirecrawlApp
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
    
def main():
    llm = LLMWrapper()
    scraper = Scrape(llm)
    arxiv_t2t = scraper.get_arxiv_content()
    news_t2t = scraper.get_markdown_content(scraper.embed.news_topics, "news")
    web_t2t = scraper.get_markdown_content(scraper.embed.tutorial_topics, "web")
    exit()
    articles = llm.make_articles(topic_to_text)
    for topic, article in articles.items():
        send_email("anantk2006@gmail.com", f"Newsletter for {topic}", article[0])
    
if __name__ == "__main__":
    main()