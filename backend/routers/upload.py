from fastapi import APIRouter, UploadFile
import os
from backend.core.rag import store_pdf

router = APIRouter()

LAST_IMAGE_FILE = "backend/storage/uploads/last_image.txt"
UPLOAD_DIR = "backend/storage/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile):
    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    chunks = store_pdf(path)
    return {"message": "PDF processed", "chunks": chunks}


@router.post("/upload/image")
async def upload_image(file: UploadFile):
    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    with open(LAST_IMAGE_FILE, "w") as f:
        f.write(file.filename)

    return {"message": "Image uploaded", "path": path}

