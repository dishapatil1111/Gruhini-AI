from rag.embedder import build_index, embed_query
import numpy as np

# Load knowledge
with open("rag/knowledge.txt", "r", encoding="utf-8") as f:
    docs = [line.strip() for line in f if line.strip()]

# Build search index
index, doc_embeddings = build_index(docs)

def retrieve(query, top_k=3):
    q_embedding = embed_query(query)

    distances, indices = index.search(np.array(q_embedding), top_k)

    results = [docs[i] for i in indices[0]]

    return results