from rag.embeddings import EmbeddingService
from rag.vector_store import VectorStore
import os

class KnowledgeBase:
    def __init__(self, index_path="data/faiss_index"):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore(index_path=index_path)

    def add_trader_profile(self, wallet, statistics, niche):
        """
        Embeds the trader profile for similarity search.
        """
        profile_text = f"Trader {wallet} specializes in {niche}. Stats: {statistics}"
        embedding = self.embedding_service.get_embeddings(profile_text)
        metadata = {
            "wallet": wallet,
            "statistics": statistics,
            "niche": niche,
            "type": "trader"
        }
        self.vector_store.add(embedding, metadata)
        self.vector_store.save()

    def query_traders(self, query):
        """
        Finds the most similar traders based on query.
        """
        query_embedding = self.embedding_service.get_embeddings(query)
        return self.vector_store.search(query_embedding)
