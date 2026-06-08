from core.orchestrator import Orchestrator
from core.node_registry import NodeRegistry
from core.agent import Agent

WORKFLOWS = {
    "recon": {
        "description": "Collect reconnaissance data from the environment.",
        "steps": [
            {"action": "scan", "target": "network"},
            {"action": "analyze", "target": "scan-results"}
        ]
    },
    "scanning": {
        "description": "Execute a scanning workflow against the selected target.",
        "steps": [
            {"action": "scan", "target": "target"},
            {"action": "analyze", "target": "target"}
        ]
    },
    "exploitation": {
        "description": "Execute an exploitation workflow against a target payload.",
        "steps": [
            {"action": "analyze", "target": "target"},
            {"action": "execute", "target": "target"}
        ]
    },
    "reporting": {
        "description": "Compile workflow results into a report.",
        "steps": [
            {"action": "analyze", "target": "results"},
            {"action": "execute", "target": "report"}
        ]
    },
    "camera_discovery": {
        "description": "Discover and enumerate IP cameras on a network.",
        "steps": [
            {"action": "scan", "target": "network", "tool": "discover_cameras", "args": {"target": "{target}"}},
            {"action": "analyze", "target": "camera-scan-results"},
            {"action": "report", "target": "cameras-found"}
        ]
    },
    "network_security_audit": {
        "description": "Perform a comprehensive network security audit including host and camera discovery.",
        "steps": [
            {"action": "scan", "target": "network-targets", "tool": "scan_network", "args": {"target": "{target}"}},
            {"action": "scan", "target": "camera-targets", "tool": "discover_cameras", "args": {"target": "{target}"}},
            {"action": "analyze", "target": "audit-results"},
            {"action": "report", "target": "security-audit"}
        ]
    },
    "rf_signal_analysis": {
        "description": "Scan for RF signals and anomalies in the environment.",
        "steps": [
            {"action": "scan", "target": "rf-spectrum", "tool": "scan_rf_signals", "args": {"frequency": "433"}},
            {"action": "analyze", "target": "rf-results"},
            {"action": "report", "target": "rf-findings"}
        ]
    },
    "firmware_threat_check": {
        "description": "Analyze firmware against known malicious signatures.",
        "steps": [
            {"action": "analyze", "target": "firmware-hash", "tool": "analyze_firmware", "args": {"firmware_hash": "{target}"}},
            {"action": "report", "target": "threat-assessment"}
        ]
    }
}

class WorkflowManager:
    def __init__(self):
        self.registry = NodeRegistry()
        self.registry.register(Agent(name="local-agent"))
        self.registry.register(Agent(name="kali-node", endpoint="http://kali-node:8001"))
        self.registry.register(Agent(name="ubuntu-node", endpoint="http://ubuntu-node:8001"))
        self.orchestrator = Orchestrator()

    def list_workflows(self):
        return [{"workflow_id": wf_id, **info} for wf_id, info in WORKFLOWS.items()]

    def execute_workflow(self, workflow_id: str, target: str | None = None):
        workflow = WORKFLOWS[workflow_id]
        steps = []
        for step in workflow["steps"]:
            step_copy = step.copy()
            if target and "{target}" in step_copy["target"]:
                step_copy["target"] = step_copy["target"].format(target=target)
            elif target and step_copy["target"] == "target":
                step_copy["target"] = target
            steps.append(step_copy)

        plan = {"goal": workflow_id, "steps": steps}
        plan = self.orchestrator.apply_policy(plan)
        scheduled_steps = self.orchestrator.schedule(plan)
        node = self.registry.select_node()

        results = []
        for step in scheduled_steps:
            results.append(self.orchestrator.dispatch_step(step, node))

        return {
            "workflow_id": workflow_id,
            "description": workflow["description"],
            "target": target,
            "results": results
        }
