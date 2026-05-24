from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_documents():

    with open("knowledge.txt", "r", encoding="utf-8") as f:
        text = f.read()

    chunks = text.split("\n")

    embeddings = model.encode(chunks)

    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    return chunks, index

chunks, index = load_documents()

def search(question):

    q_emb = model.encode([question])

    D, I = index.search(np.array(q_emb), k=3)

    results = []

    for i, score in zip(I[0], D[0]):

        results.append({
            "text": chunks[i],
            "score": float(score)
        })

    return results