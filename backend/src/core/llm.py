import os
from typing import Any, Dict, Optional


class LLMClient:
    def __init__(self, provider: str = "local", api_key: str | None = None):
        self.provider = provider
        self.api_key = api_key or os.getenv("LLM_API_KEY")

    def generate(self, prompt: str, max_tokens: int = 256, temperature: float = 0.2) -> str:
        if self.provider == "openai":
            try:
                import openai
            except ImportError:
                return self._stub_response(prompt)
            if not self.api_key:
                raise ValueError("OpenAI API key required for provider 'openai'")
            openai.api_key = self.api_key
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].text.strip()

        return self._stub_response(prompt)

    def create_plan(self, goal: str) -> Dict[str, Any]:
        if self.provider == "openai" and self.api_key:
            prompt = self._build_plan_prompt(goal)
            text = self.generate(prompt)
            return self._parse_plan_text(text, goal)

        return self._stub_plan(goal)

    def _build_plan_prompt(self, goal: str) -> str:
        return (
            f"You are an automation planner. Create a JSON plan for the goal: {goal}. "
            "Include a goal string and a list of steps. Each step must have action, target, "
            "and optionally tool or args. Do not include any unsafe shell operations."
        )

    def _parse_plan_text(self, text: str, goal: str) -> Dict[str, Any]:
        try:
            import json

            plan = json.loads(text)
            if isinstance(plan, dict) and "steps" in plan:
                return plan
        except Exception:
            pass
        return self._stub_plan(goal)

    def _stub_plan(self, goal: str) -> Dict[str, Any]:
        normalized = goal.lower()
        if any(keyword in normalized for keyword in ["scan", "network", "camera", "ip camera", "rtsp"]):
            target = self._extract_target(goal)
            return {
                "goal": goal,
                "steps": [
                    {"action": "analyze", "target": f"Assess {goal}"},
                    {
                        "action": "scan",
                        "target": target or "127.0.0.1",
                        "tool": "run_shell",
                        "args": {"command": f"nmap -sS {target or '127.0.0.1'}"},
                    },
                    {"action": "report", "target": goal},
                ],
            }

        return {
            "goal": goal,
            "steps": [
                {"action": "analyze", "target": goal},
                {
                    "action": "execute",
                    "target": goal,
                    "tool": "run_shell",
                    "args": {"command": f"echo 'Executing: {goal}'"},
                },
            ],
        }

    def _extract_target(self, goal: str) -> str | None:
        import re

        match = re.search(r"(?:on|for|target|at)\s+([\w\.-]+)", goal, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    def _stub_response(self, prompt: str) -> str:
        return "{\"goal\": \"stub\", \"steps\": [{\"action\": \"analyze\", \"target\": \"stub\"}]}"
