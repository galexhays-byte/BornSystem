from fastapi import FastAPI
from pydantic import BaseModel
import time

app = FastAPI(title="Kali Node")

class Step(BaseModel):
    action: str
    target: str

@app.get("/health")
def health():
    return {"status": "ok", "node": "kali-node"}

@app.post("/execute")
def execute(step: Step):
    return {
        "node": "kali-node",
        "step": step.dict(),
        "status": "complete",
        "timestamp": time.time()
    }
