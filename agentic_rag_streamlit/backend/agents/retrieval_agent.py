from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from document_store import DocumentStore

class RetrievalAgent:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = faiss.IndexFlatL2(384)
        self.store = DocumentStore()
        self.embeddings = []

    def embed_and_store(self, chunks):
        vectors = self.model.encode(chunks)
        self.embeddings.extend(chunks)
        self.index.add(np.array(vectors).astype('float32'))
        self.store.add_chunks(chunks)

    def retrieve(self, query, top_k=5):
        q_vec = self.model.encode([query])[0].astype('float32')
        D, I = self.index.search(np.array([q_vec]), top_k)
        return [self.store.get_chunk(i) for i in I[0]]
