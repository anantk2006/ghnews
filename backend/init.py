import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
# Create the table
cursor.execute('''DROP TABLE IF EXISTS users''')
cursor.execute('''
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    user_email TEXT,
    access_token TEXT,
    signup_date TEXT
)
''')
# cursor.execute('''DROP TABLE IF EXISTS topics''')
# cursor.execute('''
# CREATE TABLE topics (
#     topic_id SERIAL PRIMARY KEY,
#     topic TEXT
# )
# ''')
# def get_topics_from_file():
#     with open("topics.txt") as f:
#         topics = f.read().split("), ")
#         topics = [topic.split(" (") for topic in topics if len(topic) > 2]
#         types = [topic[1].split(", ") for topic in topics]
#         topics = [topic[0] for topic in topics]
#         return topics, types            

# topics, _ = get_topics_from_file()
# for topic in topics:
#     cursor.execute('''
#     INSERT INTO topics (topic)
#     VALUES (?)
#     ''', (topic,))

# Commit the changes and close the connection
cursor.execute('''DROP TABLE IF EXISTS user_skills''')
cursor.execute('''
CREATE TABLE user_skills (
    user_id INTEGER,
    topic TEXT,
    skill_level FLOAT
)
''')

cursor.execute('''DROP TABLE IF EXISTS sessions''')
cursor.execute('''
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY
)
''')

cursor.execute('''DROP TABLE IF EXISTS articles''')
cursor.execute('''CREATE TABLE articles (
    article_id INTEGER PRIMARY KEY AUTOINCREMENT,
    article TEXT,
    title TEXT,
    rlink1 TEXT,
    rlink2 TEXT,
    rlink3 TEXT,
    rimage1 TEXT,
    rimage2 TEXT,
    rimage3 TEXT,
    rtitle1 TEXT,
    rtitle2 TEXT,
    rtitle3 TEXT,
    pub_date TEXT, 
    topic TEXT
)
''')

conn.commit()
conn.close()
