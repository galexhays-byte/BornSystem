from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
def status():
    return {
        "system": "BornSystem",
        "status": "operational",
        "components": ["backend", "frontend", "nodes"]
    }
