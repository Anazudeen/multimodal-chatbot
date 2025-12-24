import faiss
import numpy as np
import pdfplumber
import json
import os
from backend.core.embedding import embed_text

INDEX_PATH = "backend/storage/faiss_index/index.bin"
CHUNKS_PATH = "backend/storage/faiss_index/chunks.json"
os.makedirs("backend/storage/faiss_index", exist_ok=True)


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"
    return text


def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]


def store_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)

    # Save chunks
    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    embeddings = embed_text(chunks).astype("float32")

    # Normalize for cosine similarity
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)   
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)

    return len(chunks)


def retrieve(query, top_k=3):
    if not os.path.exists(INDEX_PATH):
        return []

    query_emb = embed_text([query]).astype("float32")
    query_emb = query_emb / np.linalg.norm(query_emb, axis=1, keepdims=True)

    index = faiss.read_index(INDEX_PATH)
    scores, ids = index.search(query_emb, top_k)

    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    results = []
    for score, idx in zip(scores[0], ids[0]):
        if idx < len(chunks):
            results.append({
                "text": chunks[idx],
                "score": float(score)   
            })

    return results
