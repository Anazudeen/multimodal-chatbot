from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2",trust_remote_code=True)


def embed_text(texts):
    return embedder.encode(texts)
