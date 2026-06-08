from fastapi import FastAPI
from backend.api.example import router as example_router
from backend.api.system import router as system_router
from backend.api.nodes import router as nodes_router

app = FastAPI()

# Register API routes
app.include_router(example_router, prefix="/api")
app.include_router(system_router, prefix="/api")
app.include_router(nodes_router, prefix="/api/nodes")

@app.get("/health")
def health_check():
    return {"status": "ok", "system": "BornSystem Backend (Python)"}
