from openai import OpenAI
OPENAI_API_KEY = "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"
class LLMWrapper:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.critic_client = OpenAI(api_key="sk-82f67e287ba046efbf85a6b8d43ab517", base_url="https://api.deepseek.com/v1")
    def complete(self, model, messages):
        if model == "gpt-4o-mini":
            client = self.client
        else:
            client = self.critic_client
        messages = [{"role": "system", "content": "You are a helpful assistant. Be concise in your answers and do not give intros or conclusions. Just answer the questions in the specified format"},] + messages
        completion = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return completion.choices[0].message.content
    
    def critic_complete(self, messages):
        unfiltered = self.complete('deepseek-chat', messages)
        nm = messages + [
            {'role': 'assistant', 'content': unfiltered},
            {'role': 'system', 'content': 'Write a simple, few bullet point critique of the article. Ensure that the critique is constructive and helpful. Do not include any fluff or unnecessary information. Be concise and to the point. Ensure it is clear enough for a software engineer to understand.'}, 
              ]
        critique = self.complete('gpt-4o-mini', nm)
        nm = messages + [nm[0]] + [{'role': 'user', 'content': critique}] + [{'role': 'system', 'content': 'Incorporate the feedback that is valuable and relevant into the article. Ensure that the article is improved and that the feedback is integrated in a way that makes sense. Make sure the article sounds insightful and professional, like a news reporter wrote it. Keep the response fairly brief'}]
        return self.complete('deepseek-chat', nm)


    def get_topics(self, packages):
        messages = [{"role": "user", "content": f"Generate a list of 30-40 topics pertaining to the following packages. These could be anything about any computer science/engineering topic. Include nothing but the list itself in comma seperated and unordered format e.g. topic 1, topic 2, topic 3, topic 4. Each topic should be broad--there should be tech updates and news related to them. Some packages are going to be mundane--like utils or requests or json. \n Here are the packages: {packages}. What topics relate to these packages?"},]
        return self.complete("gpt-4o-mini", messages).split(", ")
    
    def analyze_readmes(self, readmes):
        batches = [readmes[i:i+5] for i in range(0, len(readmes), 5)]
        strings = ["\n\n".join(batch) for batch in batches]
        topics = []
        for string in strings:
            messages = [{"role": "user", "content": f"Analyze the README file given and provide a list of 15-20 tech news, research, and computer science topics of relevance in a comma-seperated and unordered format e.g. topic 1, topic 2, topic 3, etc. I am going to use these topics to webscrape, so make sure that they would have news/tutorials/specific articles relating to them that would interesting to software developers. Here is the file: {string}"},]
            topics += self.complete("gpt-4o-mini", messages).split(", ")
        return topics
    
    def classify_importance(self, title, prompt):
        messages = [{"role": "user", "content": f"{prompt}. Here is the title:\n{title}.\n Respond with 1 if it is good/useful and 2 if it is not, and say nothing else."},]
        out = self.complete("gpt-4o-mini", messages)
        if "1" in out and "2" not in out:
            return True
        elif "2" in out and "1" not in out:
            return False
        else: return False

    def classify_importance_web(self, title):
        prompt = "Classify whether the following title is interesting or not. Interesting involves some cool software or technique--it could include startup/company announcements, a research paper, open-source progress, news about recent government action, or a useful and cool tutorial that isn't very simple. These titles will be sent to software engineers--They should find it insightful, helpful, and non-redundant. It should not be common knowledge in the tech sphere."
        return self.classify_importance(title, prompt)

    def classify_importance_news(self, title):
        prompt = "Classify whether the following news title is interesting or not. Interesting involves some cool software or technique--it could include startup/company announcements, open-source progress, news about recent government action, etc. These titles will be sent to software engineers--They should find it insightful, helpful, and non-redundant. Note that if the title is not news, then it is not interesting and should classified as such. Titles that involve summary lists or broad overviews are also not interesting. The title should not be common knowledge in the tech sphere. It should not be non-specific or outdated."
        return self.classify_importance(title, prompt)
    
    def classify_importance_research(self, title):
        prompt = "Classify whether the following research paper title is interesting/important or not. These papers come from Arxiv, so many will be unpublished preprints with uninportant and arbitrary. Papers about niche applications or specific electronics are not important/interesting. Interesting/important papers will have impact. These titles will be sent to software engineers--they should find it insightful, helpful, and non-redundant. It should not be common knowledge in the tech sphere. It should not be non-specific or outdated."
        return self.classify_importance(title, prompt)
        
    
    def classify_type(self, title):
        messages = [{"role": "user", "content": f"Classify the type of the following title. The types are: 'news', 'tutorial', 'research paper', or 'other'. Here is the title:\n{title}.\n Respond with the type of the title, and say nothing else."},]
        return self.complete("gpt-4o-mini", messages)

    def make_articles(self, mds):
        articles = []
        print("Generating articles")
        for text in mds:
            messages = [{"role": "user", "content": f"Generate a concise news article (2 paragraphs) about the text. Here it is: {text} \n\n Make sure the article is informative and includes all the important points. Be very detailed and go into technical depth. Write it as a news summary designed for a software engineer. The article should be in markdown format. Write it formally--without bullet point lists or subheadings. Emphasize impact of the development."},]
            article = self.critic_complete(messages)
            articles.append(article)          
        return articles
    
    def make_research_summaries(self, mds):
        articles = []
        print("Generating articles")
        for text in mds:
            messages = [{"role": "user", "content": f"Generate a concise and brief (1-2 paragraphs) article about the abstract. Here it is: {text} \n\n Make sure the summary is informative and includes all the important points. Go into some amount of technical depth. Write about a) the current state of the field, b) how the article changes it in approach, c) how this will impact the world going forward. Write it as an article with no bullet points or subheadings."},]

            article = self.critic_complete(messages)
            articles.append(article)
      
        return articles



