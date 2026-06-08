from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# In-memory node registry (temporary until database layer)
nodes = {}

class NodeRegistration(BaseModel):
    node_id: str
    name: str
    type: str
    version: str

@router.post("/register")
def register_node(data: NodeRegistration):
    nodes[data.node_id] = {
        "name": data.name,
        "type": data.type,
        "version": data.version,
        "last_seen": datetime.utcnow().isoformat(),
        "status": "online"
    }
    return {"message": "Node registered", "node": nodes[data.node_id]}

@router.get("/list")
def list_nodes():
    return nodes
class NodeHeartbeat(BaseModel):
    node_id: str

@router.post("/heartbeat")
def node_heartbeat(data: NodeHeartbeat):
    if data.node_id not in nodes:
        return {"error": "Node not registered"}

    nodes[data.node_id]["last_seen"] = datetime.utcnow().isoformat()
    nodes[data.node_id]["status"] = "online"

    return {"message": "Heartbeat received", "node": nodes[data.node_id]}
def update_node_statuses():
    now = datetime.utcnow()
    for node_id, info in nodes.items():
        last_seen = datetime.fromisoformat(info["last_seen"])
        diff = (now - last_seen).total_seconds()

        if diff > 30:  # 30 seconds without heartbeat
            info["status"] = "offline"
