from transformers import AutoModel, AutoTokenizer
import torch
from file import File

from llm_wrapper import LLMWrapper

class CodeSage:
    def __init__(self):
        self.checkpoint = "codesage-small-v2"
        self.device = "cpu"  # for GPU usage or "cpu" for CPU usage
        self.topics = open("topics.txt").read().split(", ")
        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint, trust_remote_code=True, add_eos_token=True)
        self.model = AutoModel.from_pretrained(self.checkpoint, trust_remote_code=True).to(self.device)
        self.embeddings = self.get_embedding(self.topics)
        self.batch_size = 2

    def get_topic_similarity(self, text):
        text_embed = self.get_embedding(text)
        return self.embeddings @ text_embed.T
            
    def get_embedding(self, text):
        with torch.no_grad():
            if isinstance(text, list):
                inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=1024).to(self.device)
                # print(inputs["input_ids"].shape, inputs["attention_mask"].shape, inputs['input_ids'].max(), inputs['input_ids'].min())
                out = self.model(input_ids = inputs['input_ids'], attention_mask = inputs['attention_mask'], return_dict=True)        
            else:
                inputs = self.tokenizer.encode(text, return_tensors="pt").to(self.device)
                out = self.model(input_ids = inputs, return_dict=True)        
            code_vec = torch.nn.functional.normalize(out.pooler_output, p=2, dim=1)
            return code_vec

    def get_topics_for_user(self, user_files):
        llm = LLMWrapper()
        files = [file.content for file in user_files]
        return llm.analyze_readme(files)


        # file_embeds = []
        # while user_files:
        #     batch = user_files[:self.batch_size]
        #     user_files = user_files[self.batch_size:]
        #     file_embeds.append(self.get_topic_similarity([file.content for file in batch]))
        # file_embeds = torch.cat(file_embeds, dim=0)
        # most_liked = torch.argsort(torch.sum(file_embeds, dim=1), descending=True)
        # topics = []
        # for i in range(32):
        #     topics.append(self.topics[int(most_liked[i])])
        # return topics           
        

if __name__ == "__main__":
    codesage = CodeSage()
    files = [File("topics.py", open("topics.py").read(), "user", "repo", "sha"),
             File("newsletter.py", open("newsletter.py").read(), "user", "repo", "sha"),]
    print(codesage.get_topics_for_user(files))

            



