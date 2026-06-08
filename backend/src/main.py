from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))

from fastapi import FastAPI
from api.example import router as example_router
from api.system import router as system_router
from api.nodes import router as nodes_router
from api.workflows import router as workflows_router
from api.automation import router as automation_router

app = FastAPI(title="BornSystem Backend")

app.include_router(example_router, prefix="/api")
app.include_router(system_router, prefix="/api")
app.include_router(nodes_router, prefix="/api/nodes")
app.include_router(workflows_router, prefix="/api/workflows")
app.include_router(automation_router, prefix="/api/automation")

@app.get("/health")
def health_check():
    return {"status": "ok", "system": "BornSystem Backend (Python)"}
