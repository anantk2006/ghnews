from transformers import AutoModel, AutoTokenizer
import torch

class CodeSage:
    def __init__(self):
        self.checkpoint = "codesage-small-v2"
        self.device = "cpu"  # for GPU usage or "cpu" for CPU usage
        self.topics = open("topics.txt").read().split(", ")
        print(len(self.topics))
        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint, trust_remote_code=True, add_eos_token=True)
        self.model = AutoModel.from_pretrained(self.checkpoint, trust_remote_code=True).to(self.device)
        self.embeddings = self.get_embedding(self.topics)

    def get_topic_similarity(self, text):
        text_embed = self.get_embedding(text)
        print(text_embed.shape)
        return self.embeddings @ text_embed.T
            
    def get_embedding(self, text):
        inputs = self.tokenizer.encode(text, return_tensors="pt").to(self.device)
        out = self.model(inputs)
        
        vals = out.last_hidden_state[0]
        print(out.last_hidden_state.shape)
        return vals

    def get_topics_for_user(self, user_files):
        for file in user_files:
            similarities = self.get_topic_similarity(file.content)  

if __name__ == "__main__":
    codesage = CodeSage()
    print(codesage.get_topic_similarity(["Finetuning ChatGPT for a new task"]))

            



