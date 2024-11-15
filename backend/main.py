from fastapi import FastAPI
from fastapi import Request
import httpx
import datetime
import sqlite3
app = FastAPI()
async def get_access_token(code):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": "Iv23liyZsfVUeLCoHC5L",
                "client_secret": "8f4fac87460c74fa1c34635ba9dfad9af0107ffa",
                "code": code,
            }
        )
        return response.json()['access_token']
async def get_email(access_token):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user/emails",
            headers={"Authorization": f"token {access_token}"}
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
    INSERT INTO users (access_token, signup_date, user_email)
    VALUES (?, ?, ?)
    ''', (access_token, date_time, user_email))
    conn.commit()
    conn.close()

    
    
    

    