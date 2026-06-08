from fastapi import FastAPI
from pydantic import BaseModel
import time

app = FastAPI(title="Ubuntu Node")

class Step(BaseModel):
    action: str
    target: str

@app.get("/health")
def health():
    return {"status": "ok", "node": "ubuntu-node"}

@app.post("/execute")
def execute(step: Step):
    return {
        "node": "ubuntu-node",
        "step": step.dict(),
        "status": "complete",
        "timestamp": time.time()
    }
