# BornSystem Backend - Python Entry Point

from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok", "system": "BornSystem Backend (Python)"}

