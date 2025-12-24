import base64
import os
import requests
import mimetypes
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "nvidia/nemotron-nano-12b-v2-vl:free"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:5174",
    "X-Title": "Multimodal Chatbot"
}

REASONING_MEMORY = []


def call_llm(prompt, image_path=None):
    global REASONING_MEMORY

    content = [{"type": "text", "text": prompt}]


    if image_path and os.path.exists(image_path):

        # detect file type
        mime, _ = mimetypes.guess_type(image_path)
        if mime is None:
            mime = "image/png"

        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()


        content.append({
            "type": "image_url",
            "image_url": f"data:{mime};base64,{b64}"
        })


    messages = []

    if REASONING_MEMORY:
        messages.extend(REASONING_MEMORY)

    messages.append({"role": "user", "content": content})

    payload = {
        "model": MODEL,
        "messages": messages,
        "reasoning": {"enabled": True}
    }

    resp = requests.post(BASE_URL, headers=HEADERS, json=payload)

    print("\n--- DEBUG ---")
    print(resp.text)
    print("-------------\n")

    resp.raise_for_status()

    data = resp.json()
    msg = data["choices"][0]["message"]

    REASONING_MEMORY.append({
        "role": "assistant",
        "content": msg.get("content"),
        "reasoning_details": msg.get("reasoning_details")
    })

    return msg.get("content")
