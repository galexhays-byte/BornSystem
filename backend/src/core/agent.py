import json
import urllib.request
import urllib.error
from typing import Optional

from .tool_adapter import ToolAdapter


class Agent:
    def __init__(self, name: str = "local-agent", endpoint: Optional[str] = None, tool_adapter: Optional[ToolAdapter] = None):
        self.name = name
        self.endpoint = endpoint
        self.tool_adapter = tool_adapter

    def execute(self, step: dict) -> dict:
        if self.endpoint:
            payload = json.dumps(step).encode("utf-8")
            request = urllib.request.Request(
                self.endpoint + "/execute",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            try:
                with urllib.request.urlopen(request, timeout=10) as response:
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                return {
                    "node": self.name,
                    "step": step,
                    "status": "failed",
                    "error": exc.read().decode("utf-8")
                }
            except Exception as exc:
                return {
                    "node": self.name,
                    "step": step,
                    "status": "failed",
                    "error": str(exc)
                }

        if not self.tool_adapter:
            return {"node": self.name, "step": step, "status": "skipped", "message": "No local tool adapter available"}

        tool_name = step.get("tool") or "run_shell"
        args = step.get("args") or {}

        if step.get("action") == "shell" or tool_name == "run_shell":
            if "command" not in args and step.get("target"):
                args = {"command": step["target"], **args}

        return self.tool_adapter.execute(tool_name, args)
