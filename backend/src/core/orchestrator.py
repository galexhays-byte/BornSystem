from .llm import LLMClient
from .policy import PolicyEngine
from .tool_adapter import ToolAdapter


class Orchestrator:
    def __init__(self, llm_client: LLMClient | None = None, tool_adapter: ToolAdapter | None = None):
        self.policy = PolicyEngine()
        self.llm = llm_client or LLMClient()
        self.tool_adapter = tool_adapter or ToolAdapter()

    def plan(self, goal: str) -> dict:
        plan = self.llm.create_plan(goal)
        return self.apply_policy(plan)

    def apply_policy(self, plan: dict) -> dict:
        return self.policy.apply(plan)

    def schedule(self, plan: dict) -> list:
        return plan.get("steps", [])

    def dispatch_step(self, step: dict, node):
        if node and hasattr(node, "execute"):
            return node.execute(step)

        if step.get("tool"):
            return self.tool_adapter.execute(step["tool"], step.get("args"))

        return {
            "status": "skipped",
            "step": step,
            "message": "No execution path available",
        }

    def list_tools(self) -> dict:
        return {
            name: {
                "description": data["description"],
                "presets": data.get("presets", {}),
            }
            for name, data in self.tool_adapter.tools.items()
        }
