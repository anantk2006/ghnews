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

def get_repos(access_token):
    response = requests.get(
        "https://api.github.com/user/repos",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    repo_data = response.json()
    repos = []
    for repo in repo_data:
        repos.append((repo['name'], repo['default_branch']))
    return repos

def get_file_contents(user_name, access_token, repos):
    for repo_name, sha in repos:
        response = requests.get(f"https://api.github.com/repos/{user_name}/{repo_name}/git/trees/{sha}?recursive=true",
                                headers={"Authorization": f"Bearer {access_token}"})
        
@app.post("/api/register")
async def register(request: Request):
    data = await request.json()
    code = data.get("code")
    access_token = get_access_token(code)
    username, user_email = get_username_and_email(access_token)
    upload_user_to_db(username, user_email, access_token)

    repos = get_repos(access_token)
    





    
    
    
    

    


    
    

    