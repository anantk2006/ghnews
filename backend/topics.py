from transformers import AutoModel, AutoTokenizer
import torch

class CodeSage:
    def __init__(self):
        self.checkpoint = "codesage-small-v2"
        self.device = "cpu"  # for GPU usage or "cpu" for CPU usage
        self.topics = open("topics.txt").read().split(", ")
        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint, trust_remote_code=True, add_eos_token=True)
        self.model = AutoModel.from_pretrained(self.checkpoint, trust_remote_code=True).to(self.device)
        self.topic_to_embed = self.embed_topics()
    def get_similarities(self, text):
        text_embed = self.get_embedding(text)
        for topic, topic_embed in self.topic_to_embed.items():
            similarity = torch.cosine_similarity(text_embed, topic_embed, dim=0)
                        
    def embed_topics(self):
        embeddings = {}
        for topic in self.topics:
            embedding = self.get_embedding(topic)
            embeddings[topic] = embedding
        return embeddings
    def get_embedding(self, text):
        inputs = self.tokenizer.encode(text, return_tensors="pt").to(self.device)
        return self.model(inputs)[0][0][-1]

checkpoint = "codesage-small-v2"
device = "cpu"  # for GPU usage or "cpu" for CPU usage

# Note: CodeSage requires adding eos token at the end of each tokenized sequence 

tokenizer = AutoTokenizer.from_pretrained(checkpoint, trust_remote_code=True, add_eos_token=True)

model = AutoModel.from_pretrained(checkpoint, trust_remote_code=True).to(device)

inputs = tokenizer.encode("def print_hello_world():\tprint('Hello World!')", return_tensors="pt").to(device)
embedding = model(inputs)[0][0]

inputs2 = tokenizer.encode("Hello World", return_tensors="pt").to(device)
embedding2 = model(inputs2)[0][0]

for i, e1 in enumerate(embedding):
    for j, e2 in enumerate(embedding2):
        print(torch.cosine_similarity(e1, e2, dim=0))



