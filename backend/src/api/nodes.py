from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.system import BornSystem

class ExecuteNodeRequest(BaseModel):
    action: str
    target: str
    node_name: str | None = None

router = APIRouter()
system = BornSystem()

@router.get("/list")
def list_nodes():
    return {
        "nodes": [
            {"name": node.name, "endpoint": getattr(node, "endpoint", None)}
            for node in system.registry.list_nodes()
        ]
    }

@router.post("/execute")
def execute_node(request: ExecuteNodeRequest):
    if not request.action or not request.target:
        raise HTTPException(status_code=400, detail="Action and target are required")

    goal = f"{request.action}:{request.target}"
    try:
        result = system.run(goal, node_name=request.node_name)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return result
