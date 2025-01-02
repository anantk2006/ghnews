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
        messages = [{"role": "user", "content": f"Classify whether the following title is related to recent tech news or some technological update or if it is an old or unimportant article. Here is the title: {title}. Respond with 1 for the former and 2 for the latter, and say nothing else."},]
        out = self.complete("gpt-4o-mini", messages)
        if "1" in out and "2" not in out:
            return True
        elif "2" in out and "1" not in out:
            return False
        else: return False

