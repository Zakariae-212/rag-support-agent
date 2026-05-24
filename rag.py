from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import re

model = SentenceTransformer("all-MiniLM-L6-v2")


# =========================
# 1. CHUNKING INTELLIGENT
# =========================
def split_sections(text: str):

    # découpe par titres "#"
    sections = re.split(r"\n#\s+", text)

    cleaned = []

    for sec in sections:
        sec = sec.strip()

        # ignorer sections trop petites
        if len(sec) > 30:
            cleaned.append(sec)

    return cleaned


# =========================
# 2. LOAD DOCUMENTS
# =========================
def load_documents():

    with open("knowledge.txt", "r", encoding="utf-8") as f:
        text = f.read()

    chunks = split_sections(text)

    # sécurité
    chunks = [c for c in chunks if c]

    embeddings = model.encode(chunks, normalize_embeddings=True)

    dim = embeddings.shape[1]

    index = faiss.IndexFlatIP(dim)  # cosine similarity

    index.add(np.array(embeddings, dtype=np.float32))

    return chunks, index


chunks, index = load_documents()


# =========================
# 3. SEARCH FUNCTION
# =========================
def search(question):

    q_emb = model.encode([question], normalize_embeddings=True)

    D, I = index.search(np.array(q_emb, dtype=np.float32), k=5)

    results = []

    for i, score in zip(I[0], D[0]):

        if i == -1:
            continue

        # filtre de pertinence
        if score > 0.25:

            results.append({
                "text": chunks[i],
                "score": float(score)
            })

    return results