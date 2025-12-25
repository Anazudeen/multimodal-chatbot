import faiss
import numpy as np
import pdfplumber
import json
import os
from backend.core.embedding import embed_text

INDEX_PATH = "backend/storage/faiss_index/index.bin"
CHUNKS_PATH = "backend/storage/faiss_index/chunks.json"
INDEXED_PDFS_PATH = "backend/storage/faiss_index/indexed_pdfs.json"

os.makedirs("backend/storage/faiss_index", exist_ok=True)


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"
    return text


def chunk_text(text, chunk_size=500):
    words = text.split()
    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]


def load_indexed_pdfs():
    if not os.path.exists(INDEXED_PDFS_PATH):
        return set()
    with open(INDEXED_PDFS_PATH, "r") as f:
        return set(json.load(f))


def save_indexed_pdfs(pdfs):
    with open(INDEXED_PDFS_PATH, "w") as f:
        json.dump(list(pdfs), f)


def store_pdf(pdf_path):
    pdf_name = os.path.basename(pdf_path)
    indexed_pdfs = load_indexed_pdfs()

    # 🚫 DUPLICATE PDF CHECK
    if pdf_name in indexed_pdfs:
        return {
            "status": "skipped",
            "reason": "PDF already indexed",
            "pdf": pdf_name
        }

    text = extract_text_from_pdf(pdf_path)
    raw_chunks = chunk_text(text)

    chunks = [
        {"text": chunk, "source": pdf_name}
        for chunk in raw_chunks
    ]

    # Load existing chunks
    existing_chunks = []
    if os.path.exists(CHUNKS_PATH):
        with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
            existing_chunks = json.load(f)

    all_chunks = existing_chunks + chunks

    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    # 🔹 EMBEDDINGS (TEXT ONLY)
    texts = [c["text"] for c in chunks]
    embeddings = embed_text(texts).astype("float32")
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    if os.path.exists(INDEX_PATH):
        index = faiss.read_index(INDEX_PATH)
    else:
        index = faiss.IndexFlatIP(embeddings.shape[1])

    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)

    indexed_pdfs.add(pdf_name)
    save_indexed_pdfs(indexed_pdfs)

    return {
        "status": "indexed",
        "pdf": pdf_name,
        "chunks_added": len(chunks)
    }


def retrieve(query, top_k=3):
    if not os.path.exists(INDEX_PATH) or not os.path.exists(CHUNKS_PATH):
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
