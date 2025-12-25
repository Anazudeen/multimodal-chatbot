from fastapi import APIRouter
from pydantic import BaseModel
from backend.core.llm import call_llm
from backend.core.rag import retrieve
import os
import json

router = APIRouter()

UPLOAD_DIR = "backend/storage/uploads"
LAST_IMAGE_FILE = "backend/storage/uploads/last_image.txt"


class ChatRequest(BaseModel):
    query: str
    image_name: str | None = None


# =========================================================
# INTENT DETECTION
# =========================================================

def is_image_query(query: str) -> bool:
    keywords = [
        "image", "photo", "picture", "shown",
        "see", "this image", "describe the image",
        "tell about the image", "what is the image"
    ]
    q = query.lower()
    return any(k in q for k in keywords)


def wants_summary(query: str) -> bool:
    keywords = [
        "summarize", "summary", "overview",
        "brief summary", "what does the pdf say"
    ]
    q = query.lower()
    return any(k in q for k in keywords)


def wants_answer_with_points(query: str) -> bool:
    q = query.lower()
    return "key point" in q and not wants_summary(q)


def requires_pdf(query: str) -> bool:
    keywords = [
        "pdf", "document", "according to the pdf",
        "from the pdf", "in the document"
    ]
    q = query.lower()
    return any(k in q for k in keywords)


# =========================================================
# CHUNK FORMAT SAFETY
# =========================================================

def extract_chunk_text(chunk):
    if isinstance(chunk, dict):
        return chunk.get("text", "")
    return chunk


# =========================================================
# MAIN CHAT ENDPOINT
# =========================================================

@router.post("/chat")
async def chat(data: ChatRequest):

    # -------------------------
    # IMAGE HANDLING
    # -------------------------
    image_path = None

    if data.image_name:
        image_path = os.path.join(UPLOAD_DIR, data.image_name)
    elif os.path.exists(LAST_IMAGE_FILE):
        with open(LAST_IMAGE_FILE, "r") as f:
            filename = f.read().strip()
            image_path = os.path.join(UPLOAD_DIR, filename)

    image_query = is_image_query(data.query)
    summary_mode = wants_summary(data.query)
    answer_with_points_mode = wants_answer_with_points(data.query)
    force_pdf = requires_pdf(data.query)

    # -------------------------
    # RAG (PDF) — EXPLICIT ONLY
    # -------------------------
    RELEVANCE_THRESHOLD = 0.10
    relevant_chunks = []
    used_pdf = False

    if force_pdf:
        retrieval_results = retrieve(data.query)
        relevant_chunks = [
            extract_chunk_text(r["text"])
            for r in retrieval_results
            if r["score"] > RELEVANCE_THRESHOLD
        ]
        used_pdf = len(relevant_chunks) > 0

    pdf_context = "\n\n".join(relevant_chunks) if used_pdf else "None"

    # -------------------------
    # PROMPT (UNAMBIGUOUS)
    # -------------------------
    prompt = f"""
You are a multimodal AI assistant.

You MUST respond ONLY in valid JSON.
Do NOT use markdown.
Do NOT add extra text.

Universal response schema:
{{
  "summary": string | null,
  "key_points": ["string"],
  "answer": string | null,
  "used_context": {{
    "pdf": true | false,
    "image": true | false,
    "text_only": true | false
  }},
  "confidence": "low | medium | high"
}}

User query:
{data.query}

PDF context:
{pdf_context}

STRICT FORMAT RULES:
- summary_mode = {summary_mode}
- answer_with_points_mode = {answer_with_points_mode}

OUTPUT RULES:
- If summary_mode = true:
    - summary MUST be non-null
    - key_points MUST be non-empty
    - answer MUST be null

- If answer_with_points_mode = true:
    - answer MUST be non-null
    - key_points MUST be non-empty
    - summary MUST be null

- If summary_mode = false AND answer_with_points_mode = false:
    - answer MUST be non-null
    - summary MUST be null
    - key_points MUST be empty

CONTEXT RULES:
- Use PDF context ONLY if the user explicitly asks for the PDF
- If PDF context is None or insufficient, answer using general knowledge
- Never return null answers for general knowledge questions
- Do NOT mix PDF concepts into image-only answers
"""

    # -------------------------
    # LLM CALL
    # -------------------------
    raw_answer = call_llm(prompt, image_path=image_path)

    # -------------------------
    # JSON CLEANING
    # -------------------------
    def clean_llm_json(raw: str):
        raw = raw.strip()
        if raw.startswith("```"):
            parts = raw.split("```")
            if len(parts) > 1:
                raw = parts[1]
        if raw.lower().startswith("json"):
            raw = raw[4:].strip()
        return raw

    # -------------------------
    # SAFE PARSING
    # -------------------------
    try:
        cleaned = clean_llm_json(raw_answer)
        structured = json.loads(cleaned)
        if isinstance(structured, str):
            structured = json.loads(structured)

    except Exception:
        structured = {
            "summary": None,
            "key_points": [],
            "answer": raw_answer,
            "used_context": {
                "pdf": used_pdf,
                "image": image_path is not None,
                "text_only": not used_pdf and image_path is None,
            },
            "confidence": "low",
        }

    return structured
