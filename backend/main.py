from fastapi import FastAPI
from backend.api.example import router as example_router

app = FastAPI()

# Register API routes
app.include_router(example_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "system": "BornSystem Backend (Python)"}
