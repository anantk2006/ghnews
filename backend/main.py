from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import datetime
import sqlite3
import base64
import stripe

from file import File
from topics import CodeSage
from llm_wrapper import LLMWrapper


app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8000",
    "*", # for production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stripe.api_key = 'sk_test_51QbcO9RpVERX1hynlK0Vx8QjZbR3XcGMmdoaV0rNYtyiSSErUa6YsjKbRfkZR9QQ4wZyawjYyIB771jqTrvG3jYy00tfJmgeeQ'
codesage = CodeSage()
llm = LLMWrapper()
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
        if int(repo['updated_at'][2:4]) > 21:
            repos.append((repo['name'], repo['default_branch'], repo['owner']['login']))
    return repos

def get_file_links(access_token, repos):
    for repo_name, sha, owner in repos:
        response = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}/git/trees/{sha}?recursive=true",
                                headers={"Authorization": f"Bearer {access_token}"})
        tree_data = response.json()
        yield tree_data, owner, repo_name, sha

def get_commit_history(access_token, owner, repo, email):
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/commits?author={email}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    commit_data = response.json()
    for commit in commit_data:
        if commit['commit']['committer']['date'][2:4] > 21:
            return commit['message']

def get_file_contents(access_token, owner, repo, path, sha):
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={sha}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    file_data = response.json()
    return file_data

def retrieve_user_content(access_token, repos):
    decode = lambda s: base64.b64decode(s['content']).decode('utf-8')
    # check_path = lambda s: s.endswith('.py') or s.endswith('.js') or s.endswith('.ts') \
    #                    or s.endswith(".cpp") or s.endswith('.rs')
    check_path_readme = lambda s: s.endswith("README.md") or s.endswith("readme.md")
    # files_code = []
    files_readme = []
    for tree, owner, repo_name, sha in get_file_links(access_token, repos):
        try:
            tree = tree['tree']
        except KeyError:
            continue
        for file in tree:
            readme = check_path_readme(file['path'])
            if readme:
                f = get_file_contents(access_token, owner, repo_name, file['path'], sha)
                if ('message' in f and f['message'] == 'Not Found') or 'content' not in f:
                    continue
                else: 
                    # if code:
                    #     files_code.append(File(file['path'], decode(f), owner, repo_name, sha))
                    if readme:
                        files_readme.append(File(file['path'], decode(f), owner, repo_name, sha))
    return files_readme

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

def check_session_id(session_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions WHERE session_id=?", (session_id,))
    result = cursor.fetchone()
    # need to delete session id after use
    if result is not None:
        cursor.execute("DELETE FROM sessions WHERE session_id=?", (session_id,))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False
    

@app.post("/api/register")
async def register(request: Request):
    # First extract topics/packages from code
    print("Request received, starting extraction")
    data = await request.json()
    code = data.get("code")
    session_id = data.get("session_id")

    paid = check_session_id(session_id)
    if not paid:
        return {"error": "Payment required"}

    access_token = get_access_token(code)
    username, user_email = get_username_and_email(access_token)
    upload_user_to_db(username, user_email, access_token)
    repos = get_repos(access_token)   
    # Contact LLM to generate list of topics
    # Some degree of parsing should be used
    
    files_readme = retrieve_user_content(access_token, repos)
    print("Extraction complete, beginning topic generation")
    # apis = []
    # for file in files_code:
    #     for api in file.find_api():
    #         apis.append(api) 
    
    # api_topics = llm.get_topics(apis) 
    
    readme_topics = codesage.get_topics_for_user(files_readme)
    topics = list(set(readme_topics))
    print(topics)
    save_topics_to_db(username, topics)

def save_session_to_db(session_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO sessions (session_id)
    VALUES (?)
    ''', (session_id,))
    conn.commit()
    conn.close()

@app.post('/api/pay')
def create_payment_intent(request: Request):
    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": 'price_1QbcQPRpVERX1hynqpNtMWed', "quantity": 1}],
        ui_mode="embedded",
        return_url="http://localhost/paid?session_id={CHECKOUT_SESSION_ID}",
    )
    session_id = session.id
    save_session_to_db(session_id)
    return session.client_secret



    

    
        
        


    





    
    
    
    

    


    
    

    