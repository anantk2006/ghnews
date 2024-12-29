import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
# Create the table
cursor.execute('''DROP TABLE IF EXISTS users''')
cursor.execute('''
CREATE TABLE users (
    username TEXT,
    user_email TEXT PRIMARY KEY,
    access_token TEXT,
    signup_date TEXT
)
''')

# Commit the changes and close the connection
cursor.execute('''DROP TABLE IF EXISTS topics''')
cursor.execute('''
CREATE TABLE topics (
    username TEXT,
    topic TEXT
)
''')
cursor.execute('''DROP TABLE IF EXISTS links''')
cursor.execute('''
CREATE TABLE links (
    topic TEXT,
    link TEXT
)
''')
conn.commit()
conn.close()
