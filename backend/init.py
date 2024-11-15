import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    access_token TEXT,
    signup_date TEXT,
    user_email TEXT
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
