from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Literal
from function.func import *
import json
import uvicorn

app = FastAPI(title="Encryption Server")

LOG_FILE = "logs.json"

def save_to_json(data: dict):
    try:
        with open(LOG_FILE, "r") as file:
            logs = json.load(file)
            if not isinstance(logs, list):
                logs = []
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []
    logs.append(data)

    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)


class CaesarRequest(BaseModel):
    text: str
    offset: int
    mode: Literal["encrypt", "decrypt"]


class FenceDecryptRequest(BaseModel):
    text: str



@app.get("/logs")
async def get_logs():
    try:
        with open(LOG_FILE, "r") as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []
    return {"logs": logs}


@app.post("/caesar")
async def caesar_cipher(request: CaesarRequest):
    if request.mode == "encrypt":
        result = caesar_encrypt(request.text, request.offset)
        save_to_json({"type": "caesar_encrypt", "text": request.text, "offset": request.offset, "result": result})
        return {"encrypted_text": result}
    else:
        result = caesar_decrypt(request.text, request.offset)
        save_to_json({"type": "caesar_decrypt", "text": request.text, "offset": request.offset, "result": result})
        return {"decrypted_text": result}


@app.get("/fence/encrypt")
async def fence_encrypt_endpoint(text: str = Query(..., description="Text to encrypt")):
    encrypted = fence_encrypt(text)
    save_to_json({"type": "fence_encrypt", "text": text, "result": encrypted})
    return {"encrypted_text": encrypted}


@app.post("/fence/decrypt")
async def fence_decrypt_endpoint(request: FenceDecryptRequest):
    decrypted = fence_decrypt(request.text)
    save_to_json({"type": "fence_decrypt", "text": request.text, "result": decrypted})
    return {"decrypted": decrypted}


@app.get("/")
async def root():
    return {
        "message": "Encryption Server",
        "endpoints": {
            "caesar": "POST /caesar",
            "fence_encrypt": "GET /fence/encrypt?text=...",
            "fence_decrypt": "POST /fence/decrypt"
        }
    }


if __name__ == "__main__":
    uvicorn.run(app,port=8005)

