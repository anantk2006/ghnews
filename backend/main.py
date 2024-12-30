from fastapi import FastAPI
from fastapi import Request
import requests
from datetime import datetime
import sqlite3
import base64
from file import File
from llm_wrapper import LLMWrapper
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
        repos.append((repo['name'], repo['default_branch'], repo['owner']['login']))
    return repos

def get_file_links(access_token, repos):
    for repo_name, sha, owner in repos:
        response = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}/git/trees/{sha}?recursive=true",
                                headers={"Authorization": f"Bearer {access_token}"})
        tree_data = response.json()
        yield tree_data, owner, repo_name, sha

def get_file_contents(access_token, owner, repo, path, sha):
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={sha}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    file_data = response.json()
    return file_data

def retrieve_user_content(access_token, repos):
    decode = lambda s: base64.b64decode(s['content']).decode('utf-8')
    check_path = lambda s: s.endswith('.py') or s.endswith('.js') # \
                       # or s.endswith('.html') or s.endswith('.ts') \
                       # or s.endswith(".cpp") or s.endswith('.rs')
    for tree, owner, repo_name, sha in get_file_links(access_token, repos):
        try:
            tree = tree['tree']
        except KeyError:
            continue
        for num, file in enumerate(tree):
            if check_path(file['path']):
                f = get_file_contents(access_token, owner, repo_name, file['path'], sha)
                if ('message' in f and f['message'] == 'Not Found') or 'content' not in f:
                    continue
                else: yield File(file['path'], decode(f), owner, repo_name, sha)

def save_topics_to_db(username, topics):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    for topic in topics:
        cursor.execute('''
        INSERT INTO topics (username, topic)
        VALUES (?, ?)
        ''', (username, topic))
    conn.commit()
    conn.close()

@app.post("/api/register")
async def register(request: Request):
    # First extract topics/packages from code
    print("Request received, starting extraction")
    data = await request.json()
    code = data.get("code")
    access_token = get_access_token(code)
    username, user_email = get_username_and_email(access_token)
    upload_user_to_db(username, user_email, access_token)
    repos = get_repos(access_token)
    topics = []
    for file in retrieve_user_content(access_token, repos):
        for api in file.find_api():
            topics.append(api)
    
    topics = list(set(topics))
    # Contact LLM to generate list of topics
    print("Extraction complete, beginning topic generation")
    llm_wrapper = LLMWrapper()
    topics = llm_wrapper.get_topics(topics)
    save_topics_to_db(username, topics)
   
    # Search for information about each topic



    

    
        
        


    





    
    
    
    

    


    
    

    