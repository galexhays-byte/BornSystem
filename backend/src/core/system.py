import uuid
from .llm import LLMClient
from .orchestrator import Orchestrator
from .node_registry import NodeRegistry
from .agent import Agent
from .state_manager import StateManager
from .tool_adapter import ToolAdapter


class BornSystem:
    def __init__(self):
        tool_adapter = ToolAdapter()
        self.orchestrator = Orchestrator(llm_client=LLMClient(), tool_adapter=tool_adapter)
        self.registry = NodeRegistry()
        self.state = StateManager()
        self.registry.register(Agent(name="local-agent", tool_adapter=tool_adapter))
        self.registry.register(Agent(name="kali-node", endpoint="http://kali-node:8001"))
        self.registry.register(Agent(name="ubuntu-node", endpoint="http://ubuntu-node:8001"))

    def run(self, goal: str, node_name: str = None) -> dict:
        plan = self.orchestrator.plan(goal)
        steps = self.orchestrator.schedule(plan)

        results = []
        node = self.registry.select_node(node_name)
        for step in steps:
            result = self.orchestrator.dispatch_step(step, node)
            results.append(result)
            self.state.update(step["action"], result)

        run_id = str(uuid.uuid4())
        self.state.save_run(run_id, {"goal": goal, "results": results})

        return {
            "run_id": run_id,
            "goal": goal,
            "plan": plan,
            "results": results,
            "state": self.state.state,
        }
