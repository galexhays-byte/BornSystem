from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from core.system import BornSystem


class AutomationRequest(BaseModel):
    goal: str
    node_name: str | None = None


class GenerateScriptRequest(BaseModel):
    scan_result: dict
    device_info: str | None = None


class ExecuteToolRequest(BaseModel):
    tool_name: str
    args: dict | None = None


router = APIRouter()
service = BornSystem()


@router.post("/run")
def run_automation(request: AutomationRequest):
    if not request.goal:
        raise HTTPException(status_code=400, detail="goal is required")

    try:
        return service.run(request.goal, request.node_name)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/plan")
def generate_plan(request: AutomationRequest):
    if not request.goal:
        raise HTTPException(status_code=400, detail="goal is required")

    try:
        plan = service.orchestrator.plan(request.goal)
        return {"goal": request.goal, "plan": plan}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/generate_script")
def generate_script(request: GenerateScriptRequest):
    try:
        return service.orchestrator.tool_adapter.execute(
            "generate_followup_script",
            {"scan_result": request.scan_result, "device_info": request.device_info},
        )
    except KeyError:
        raise HTTPException(status_code=404, detail="Script generation tool not found")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/execute")
def execute_tool(request: ExecuteToolRequest):
    if not request.tool_name:
        raise HTTPException(status_code=400, detail="tool_name is required")

    try:
        return service.orchestrator.tool_adapter.execute(request.tool_name, request.args)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Tool '{request.tool_name}' not found")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/tools")
def list_tools():
    return {"tools": service.orchestrator.list_tools()}


@router.get("/history")
def list_history(limit: int = 50):
    try:
        runs = service.state.list_runs(limit=limit)
        return {"runs": runs}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/history/{run_id}")
def get_history_run(run_id: str):
    try:
        run = service.state.get_run(run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
        return {"run_id": run_id, "payload": run}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
