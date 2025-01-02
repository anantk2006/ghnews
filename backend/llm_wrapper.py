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
        messages = [{"role": "user", "content": f"Generate a list of 30-40 topics pertaining to the following packages. These could be anything about any computer science/engineering topic. Include nothing but the list itself in comma seperated format e.g. topic 1, topic 2, topic 3, topic 4. \n Here are the packages: {packages}"},]
        return self.complete("gpt-4o-mini", messages).split(", ")
