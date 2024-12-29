from openai import OpenAI
OPENAI_API_KEY = "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"
class LLMWrapper:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    def complete(self, model, messages):
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        return completion.choices[0].message

    def get_topics(self, packages):
        messages = [f"Generate a list of 30-40 topics pertaining to the following packages. These could be anything from graph neural networks to particular coins in the cryptocurrency space. Include nothing but the list itself. {str(packages)[1:-1]}"]
        return self.complete("gpt-4o-mini", messages)
