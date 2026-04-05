import faiss
import numpy as np
import json
import os

class VectorStore:
    def __init__(self, dimension=384, index_path="data/faiss_index"):
        self.dimension = dimension
        self.index_path = index_path
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []
        
        if os.path.exists(self.index_path):
            self.load()

    def add(self, vector, metadata_item):
        vector = np.array([vector]).astype('float32')
        self.index.add(vector)
        self.metadata.append(metadata_item)

    def search(self, query_vector, k=5):
        query_vector = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(query_vector, k)
        
        results = []
        for i in range(len(indices[0])):
            idx = indices[0][i]
            if idx != -1:
                results.append({
                    "metadata": self.metadata[idx],
                    "score": float(distances[0][i])
                })
        return results

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.index_path + "_metadata.json", "w") as f:
            json.dump(self.metadata, f)

    def load(self):
        self.index = faiss.read_index(self.index_path)
        with open(self.index_path + "_metadata.json", "r") as f:
            self.metadata = json.load(f)
