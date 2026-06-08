class PolicyEngine:
    ALLOWED_ACTIONS = {"analyze", "execute", "scan", "report"}
    DENY_TARGET_PATTERNS = ["rm -rf", "shutdown", "format ", "delete all", "drop table"]

    def apply(self, plan: dict) -> dict:
        if not isinstance(plan, dict) or "steps" not in plan:
            raise ValueError("Invalid plan structure")

        filtered_steps = []
        for step in plan["steps"]:
            action = step.get("action")
            target = step.get("target")

            if action not in self.ALLOWED_ACTIONS:
                raise ValueError(f"Disallowed action: {action}")

            if not isinstance(target, str) or not target:
                raise ValueError("Each step target must be a non-empty string")

            normalized_target = target.lower()
            for pattern in self.DENY_TARGET_PATTERNS:
                if pattern in normalized_target:
                    raise ValueError(f"Target contains forbidden operation: {target}")

            filtered_steps.append(step)

        return {**plan, "steps": filtered_steps}
