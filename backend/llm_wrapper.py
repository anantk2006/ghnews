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
        return completion.choices[0].message

    def get_topics(self, packages):
        messages = [{"role": "user", "content": "Generate a list of 30-40 topics pertaining to the following packages. These could be anything from graph neural networks to particular coins in the cryptocurrency space. Include nothing but the list itself in comma seperated format e.g. graph AI, Ethereum, Supabase, Stripe, LLaMA."},]
        return self.complete("gpt-4o-mini", messages)
