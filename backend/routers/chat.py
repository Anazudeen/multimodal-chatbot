from fastapi import APIRouter
from pydantic import BaseModel
from backend.core.llm import call_llm
from backend.core.rag import retrieve
import os

router = APIRouter()

UPLOAD_DIR = "backend/storage/uploads"
LAST_IMAGE_FILE = "backend/storage/uploads/last_image.txt"



class ChatRequest(BaseModel):
    query: str
    image_name: str | None = None


@router.post("/chat")
async def chat(data: ChatRequest):
    image_path = None
    if data.image_name:
        image_path = os.path.join(UPLOAD_DIR, data.image_name)

    elif os.path.exists(LAST_IMAGE_FILE):
        with open(LAST_IMAGE_FILE, "r") as f:
            filename = f.read().strip()
            image_path = os.path.join(UPLOAD_DIR, filename)


    # RAG Retrieval
    retrieval_results = retrieve(data.query)

    # Check if context is relevant (low distance = good match)
    RELEVANCE_THRESHOLD = 0.10  # cosine similarity threshold

    relevant_chunks = [
        r["text"] for r in retrieval_results if r["score"] > RELEVANCE_THRESHOLD
    ]

    # If no relevant chunks → skip RAG entirely
    if len(relevant_chunks) == 0:
        pdf_context = "None"
        use_rag = False
    else:
        pdf_context = "\n\n".join(relevant_chunks)
        use_rag = True

    # Build prompt
    prompt = f"""
You are a multimodal assistant.

### User Query:
{data.query}

### PDF Context (use only if helpful):
{pdf_context}

### Instructions:
- If PDF context is "None" → answer normally as a general AI assistant.
- If PDF context exists, use it first.
- If PDF context exists → use it to answer.
- Only analyze the image if the user query is about the image.
"""

    answer = call_llm(prompt, image_path=image_path)
    return {"answer": answer}

