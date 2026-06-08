from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from workflows.workflows import WorkflowManager

class WorkflowRequest(BaseModel):
    workflow_id: str
    target: str | None = None

router = APIRouter()
manager = WorkflowManager()

@router.get("/list")
def list_workflows():
    return {"workflows": manager.list_workflows()}

@router.post("/execute")
def execute_workflow(request: WorkflowRequest):
    if not request.workflow_id:
        raise HTTPException(status_code=400, detail="workflow_id is required")

    try:
        result = manager.execute_workflow(request.workflow_id, target=request.target)
    except KeyError:
        raise HTTPException(status_code=404, detail="Workflow not found")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return result
