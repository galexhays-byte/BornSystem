from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/info")
def system_info():
    return {
        "system": "BornSystem",
        "version": "0.1.0",
        "environment": "development",
        "timestamp": datetime.utcnow().isoformat(),
        "backend": "python-fastapi",
        "status": "online",
        "nodes_connected": 0  # placeholder for future node system
    }
