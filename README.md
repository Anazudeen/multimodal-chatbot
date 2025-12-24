# Multimodal Chatbot with RAG & LLM
---

## Features

- 📄 **PDF Understanding**: Upload PDFs and ask questions about the content.
- 🖼️ **Image Analysis**: Upload an image and ask questions related to it.
- 💬 **Text Queries**: Ask general questions with or without PDF/image context.
- ⚡ **RAG Pipeline**: Relevant PDF chunks retrieved via **FAISS + SentenceTransformer**.
- 🧠 **Reasoning Memory**: Maintains conversation context across queries.
- 🔗 **OpenRouter LLM Integration**: Uses free LLMs for text & multimodal reasoning.

---

## Tech Stack

- **Backend**: FastAPI, Python
- **Frontend**: React + Vite
- **Embeddings**: `SentenceTransformer` (`all-MiniLM-L6-v2`)
- **Vector Store**: FAISS
- **LLM**: OpenRouter API (`nvidia/nemotron-nano-12b-v2-vl:free`)
- **File Handling**: PDF (`pdfplumber`), Image upload
- **Environment Management**: `.env` (contains your API key)

---

## Installation
```bash

### Backend

# Start FastAPI server
python -m uvicorn backend.main:app --reload

### Frontend

cd frontend
npm install
npm run dev

---

## Project Structure:

backend/
 ├─ core/
 │   ├─ llm.py        # LLM call & reasoning memory
 │   ├─ rag.py        # FAISS embeddings & PDF retrieval
 │   └─ embedding.py  # SentenceTransformer embeddings
 ├─ routers/
 │   ├─ chat.py       # Chat API
 │   └─ upload.py     # PDF/Image upload API
 ├─ storage/
 │   ├─ faiss_index/  # FAISS index and chunks
 │   └─ uploads/      # Uploaded files
 └─ main.py           # FastAPI app
frontend/
 ├─ src/
 └─ vite.config.js

---

