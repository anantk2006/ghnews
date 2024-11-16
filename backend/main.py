from fastapi import FastAPI
from fastapi import Request
import requests
from datetime import datetime
import sqlite3
app = FastAPI()
async def get_access_token(code):
    response = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": "Iv23liyZsfVUeLCoHC5L",
            "client_secret": "8f4fac87460c74fa1c34635ba9dfad9af0107ffa",
            "code": code
        }
    )
    token_data = response.json()
    return token_data["access_token"]
async def get_email(access_token):
    response = requests.get(
        "https://api.github.com/user/emails",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    emails = response.json()
    primary_email = next(email['email'] for email in emails if email['primary'])
    return primary_email
@app.post("/api/register")
async def register(request: Request):
    data = await request.json()
    code = data.get("code")
    access_token = await get_access_token(code)
    user_email = await get_email(access_token)
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (user_email, access_token, signup_date)
    VALUES (?, ?, ?)
    ''', (user_email, access_token, date_time))


    conn.commit()
    conn.close()


    
    

    