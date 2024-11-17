from fastapi import FastAPI
from fastapi import Request
import requests
from datetime import datetime
import sqlite3
app = FastAPI()
def get_access_token(code):
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

def upload_user_to_db(username, user_email, access_token):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute('''
        INSERT INTO users (username, user_email, access_token, signup_date)
        VALUES (?, ?, ?, ?)
        ''', (username, user_email, access_token, date_time)) 
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        conn.close()
        return {"error": "User already exists"}
    
def get_username_and_email(access_token):
    response = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    user_data = response.json()
    return user_data["login"], user_data["email"]
    
@app.post("/api/register")
async def register(request: Request):
    data = await request.json()
    code = data.get("code")
    access_token = get_access_token(code)
    username, user_email = get_username_and_email(access_token)
    upload_user_to_db(username, user_email, access_token)




    
    
    
    

    


    
    

    