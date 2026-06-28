from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model (this converts text → vectors)
model = SentenceTransformer("all-MiniLM-L6-v2")

def build_index(texts):
    embeddings = model.encode(texts)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)

    index.add(np.array(embeddings))

    return index, embeddings

def embed_query(query):
    return model.encode([query])