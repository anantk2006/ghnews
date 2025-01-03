from openai import OpenAI
import openai
OPENAI_API_KEY = "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"
class LLMWrapper:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
    def complete(self, model, messages):
        messages = [{"role": "developer", "content": "You are a helpful assistant. Be concise in your answers and do not give intros or conclusions. Just answer the questions in the specified format"},] + messages
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        return completion.choices[0].message.content

    def get_topics(self, packages):
        messages = [{"role": "user", "content": f"Generate a list of 30-40 topics pertaining to the following packages. These could be anything about any computer science/engineering topic. Include nothing but the list itself in comma seperated and unordered format e.g. topic 1, topic 2, topic 3, topic 4. Each topic should be active and slightly broad--there should be tech updates and news related to them. \n Here are the packages: {packages}"},]
        return self.complete("gpt-4o-mini", messages).split(", ")
    
    def classify_importance(self, title):
        messages = [{"role": "user", "content": f"Classify whether the following title is important tech news or not. Important tech news involves some cool software or technique that is novel--it could include startup/company announcements, a research paper, interesting open-source progress, or news about recent government action. Here is the title:\n{title}.\n Respond with 1 for the former and 2 for the latter, and say nothing else."},]
        out = self.complete("gpt-4o-mini", messages)
        if "1" in out and "2" not in out:
            return True
        elif "2" in out and "1" not in out:
            return False
        else: return False

    def make_articles(self, topic_to_text):
        articles = {}
        for topic, text in topic_to_text.items():
            messages = [{"role": "user", "content": f"Generate a concise tutorial about the text. Here it is: {text} \n\n Make sure the tutorial is informative and includes all the important points. Be very detailed and go into technical depth. Write it as a brief tutorial designed for a software engineer. The article should be in markdown format."},]
            article = self.complete("gpt-4o-mini", messages)
            if topic in articles:
                articles[topic].append(article)
            else:
                articles[topic] = [article]
        return articles

