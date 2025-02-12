import sqlite3
from topics import ArcticEmbed
from llm_wrapper import LLMWrapper
from scrape import Scrape

import smtplib
from email.mime.image import MIMEImage
from email.message import EmailMessage
import datetime
import random
from scrape import GoogleNews, BingSearch
from jinja2 import Environment, FileSystemLoader

top_k_topics = 5
llm = LLMWrapper()
scrape = Scrape(llm)
google_news = GoogleNews(llm)
bing_news = BingSearch(llm)

template_loader = FileSystemLoader(searchpath="./")  # Path to your templates folder
env = Environment(loader=template_loader)

# Load the template
template = env.get_template("template.html")

def send_email(email_address, subject, text):
    # Convert markdown to HTML
    
    # Create message container
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'anantk2006@gmail.com'
    msg['To'] = email_address
    msg.add_alternative(text, subtype='html')
    
    # Record the MIME types of both parts - text/plain and text/html
    # Attach parts into message container
    with open("logo.png", "rb") as img_file:
        img = MIMEImage(img_file.read())
        img.add_header("Content-ID", "<embedded_image>")
        msg.attach(img)
    
    # Send the message via local SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("virsitilenews@gmail.com", "buei lsjm bpxf xjag")
        smtp.send_message(msg)

def retrieve_user_info():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT user_id, user_email FROM users
    ''')
   
    info = cursor.fetchall()
    emails = [email[1] for email in info if email]
    ids = [email[0] for email in info if email]
    
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
    conn.close()
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
        user_emails[user_id] = random.sample([content[topic][:2] for topic, _ in top_k], 5)
    return user_emails

def run_arxiv():
    id_to_email, user_to_topic_to_skill = retrieve_user_info()  
    llm = LLMWrapper()
    scrape = Scrape(llm)
    arxiv_abstracts = scrape.get_arxiv_content()
    # print(arxiv_abstracts)
    user_emails = match_content(user_to_topic_to_skill, arxiv_abstracts)
    user_emails = links_to_articles(user_emails, scrape_do= False)
    
    make_and_send_emails(user_emails, id_to_email, search_type="arxiv")

def text_to_articles(user_emails):
    set_of_texts = set()
    for user_id, emails in user_emails.items():
        for email in emails:
            set_of_texts.add(email)
    texts = list(set_of_texts)
    arts = llm.make_articles(texts)
    ret = {}
    for user_id, emails in user_emails.items():
        for art, text in zip(arts, texts):
            if text in emails:
                if user_id not in ret:
                    ret[user_id] = [art]
                else: ret[user_id].append(art)
    return ret

def links_to_articles(user_emails, scrape_do = True):
    links_to_user = {}
    for user_id, emails in user_emails.items():
        for email in emails:
            for link_holder in email:
                if scrape_do: link = link_holder[1]
                else: link = link_holder[1]

                r_link = link if scrape_do else link_holder[2]

                other_links = email if scrape_do else link_holder[3:]
                if link not in links_to_user:
                    links_to_user[link] = [(user_id, link_holder[0], r_link, other_links)]
                else: links_to_user[link].append((user_id, link_holder[0], r_link, other_links))
    links = list(links_to_user.keys()) 
    if scrape_do: 
        var = scrape.markdown_helper(links, "news")
        articles = llm.make_articles(var)
    else:
        articles = llm.make_research_summaries(links)    
    ret = {}
    for link, text in zip(links, articles):
        if "None" in text and len(text) < 10: continue
        for user_id, title, r_link, other_links in links_to_user[link]:
            title_str = title if scrape_do else title[6:]
            if user_id not in ret:
                ret[user_id] = [(text, title_str, r_link, other_links)]
            else: ret[user_id].append((text, title_str, r_link, other_links))  
      
    return ret

    





def run_news():
    
    id_to_email, user_to_topic_to_skill = retrieve_user_info()
    topics = random.sample(scrape.embed.news_topics, 5)
    topic_to_links = bing_news.search(topics)
    user_emails = match_content(user_to_topic_to_skill, topic_to_links)
    user_emails = links_to_articles(user_emails)
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
    if count < 200:
        ttl = scrape.ggl.find_relevant_links(topics[:5], search_type)
        scrape.add_links_to_db(ttl, search_type)
    topic_to_content = scrape.markdown_helper(topic_to_links, search_type)
    user_emails = match_content(user_to_topic_to_skill, topic_to_content)

def get_jinja_contents(emails):
    return template.render(emails = emails, date = datetime.datetime.now().strftime("%m/%d/%Y"))

def save_art_to_db(emails):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    ids = []
    for email in emails:
        others = email['others']
        rtitle1 = others[0]['title'] if len(others) > 0 else None
        rlink1 = others[0]['url'] if len(others) > 0 else None
        rtitle2 = others[1]['title'] if len(others) > 1 else None
        rlink2 = others[1]['url'] if len(others) > 1 else None
        rtitle3 = others[2]['title'] if len(others) > 2 else None
        rlink3 = others[2]['url'] if len(others) > 2 else None
        
        cursor.execute('''
        INSERT INTO articles (article, title, rlink1, rlink2, rlink3, rtitle1, rtitle2, rtitle3, pub_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (email['content'], email['title'], rlink1, rlink2, rlink3, rtitle1, rtitle2, rtitle3, email['date']))
        cursor.execute('SELECT last_insert_rowid()')
        user_id = cursor.fetchone()[0]
        ids.append(user_id)

    conn.commit()
    conn.close()
    return ids

def make_and_send_emails(user_emails, id_to_email, search_type = "news"):
    type_str = 'Curated News For You' if search_type == 'news' else 'Recent Paper Abstracts For You'
    now = datetime.datetime.now()
    formatted_date = now.strftime("%B %d, %Y %I:%M%p")
    for user_id, emails in user_emails.items():
        # if len(emails) < 2: continue
        email_address = id_to_email[user_id]
        
        if search_type == 'news':
            em = [{'content': email[0].replace("\n", "<br>") + "...",
                    'title': email[1], 'url': email[2],
                    'date': formatted_date,
                    'others': random.sample([{'title': art[0], 'url': art[1]} 
                                            for art in email[3]], 3 if len(email[3]) >=3 else len(email[3]))} 
                                            for email in emails]
        else:
            em = [{'content': email[0].replace("\n", "<br>") + "...",
                    'title': email[1], 'url': email[2],
                    'date': formatted_date,
                    'others': random.sample([{'title': art['title'], 'url': art['link']} 
                                            for art in email[3]], 3 if len(email[3]) >=3 else len(email[3]))} 
                                            for email in emails]
        
        ids = save_art_to_db(em)
        for idx, e in enumerate(em):
            e['url'] = "http://localhost/article?id=" + str(ids[idx])
        for email in em:
            email['content'] = email['content'][:300] + "..."
        contents = get_jinja_contents(em)        
        send_email(email_address, f'{type_str}', contents)  

           
    
            





def main():
    
    run_arxiv()
    run_news()

if __name__ == "__main__":
    # dummy_user_emails = {
    #     1: [
    #         ("This is a dummy article content for user 1", "Dummy Article 1", "http://example.com/1", [("Related Article 1", "http://example.com/r1"), ("Related Article 2", "http://example.com/r2")]),
    #         ("This is another dummy article content for user 1", "Dummy Article 2", "http://example.com/2", [("Related Article 3", "http://example.com/r3"), ("Related Article 4", "http://example.com/r4")])
    #     ]
    # }

    # dummy_id_to_email = {
    #     1: "anantk2006@gmail.com"
    # }

    # make_and_send_emails(dummy_user_emails, dummy_id_to_email, search_type="news")
    main()