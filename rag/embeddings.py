from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingService:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def get_embeddings(self, text):
        return self.model.encode([text])[0]

    def get_batch_embeddings(self, texts):
        return self.model.encode(texts)
