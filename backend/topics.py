from transformers import AutoModel, AutoTokenizer
import torch
from file import File
from torch.nn.functional import normalize

from llm_wrapper import LLMWrapper

class ArcticEmbed:
    def __init__(self):

        # Init info
        self.checkpoint = "Snowflake/snowflake-arctic-embed-m-v1.5"
        # Initialize topics and topic classifications
        self.topics, self.types = self.get_topics_from_file()
        self.paper_topics = [topic for topic, type in zip(self.topics, self.types) if "papers" in type]
        self.news_topics = [topic for topic, type in zip(self.topics, self.types) if "news" in type]
        self.tutorial_topics = [topic for topic, type in zip(self.topics, self.types) if "tutorial" in type]
        
        # setup the model p well
        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint)
        self.model = AutoModel.from_pretrained(self.checkpoint, add_pooling_layer=False, trust_remote_code=True)
        self.model.eval()
        self.embeddings = self.get_embedding(self.topics)
        self.paper_embeds = self.get_embedding(self.paper_topics)
    
    def get_topics_from_file(self):
        with open("topics.txt") as f:
            topics = f.read().split("), ")
            topics = [topic.split(" (") for topic in topics if len(topic) > 2]
            types = [topic[1].split(", ") for topic in topics]
            topics = [topic[0] for topic in topics]
            return topics, types            

    def get_topic_similarity(self, text):
        text_embed = self.get_embedding(text)
        return self.embeddings @ text_embed.T
            
    def get_embedding(self, text):
        with torch.no_grad():
            # Batched or unbatched input
            document_tokens =  self.tokenizer(text, 
                                              padding=True, 
                                              truncation=True, 
                                              return_tensors='pt', 
                                              max_length=8192)
            document_embeddings = self.model(**document_tokens)[0][:, 0]
            document_embeddings = torch.nn.functional.normalize(document_embeddings, p=2, dim=1)
        return document_embeddings

    def get_topics_for_user(self, user_files):
        # We first analyze the readmes that the user has uploaded
        llm = LLMWrapper()
        files = [file.content for file in user_files]
        direct_topics = llm.analyze_readmes(files)

        # We have readme topics, but we need to translate into my topics
        user_embeds = self.get_embedding(direct_topics)
        matrix = self.embeddings @ user_embeds.T # num server topics x num user topics

        # Sum across all topic similarity to our topics
        sims = torch.sum(matrix, dim=1).flatten()
        skills = sims.tolist()
        topic_to_skill = {topic: skill for topic, skill in zip(self.topics, skills)}
        return topic_to_skill
        

if __name__ == "__main__":
    codesage = ArcticEmbed()
    exit()
    files = [File("topics.py", open("topics.py").read(), "user", "repo", "sha"),
             File("newsletter.py", open("newsletter.py").read(), "user", "repo", "sha"),]
    print(codesage.get_topics_for_user(files))

            



