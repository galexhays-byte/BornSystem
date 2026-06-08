# Automation Architecture

This document describes the new BornSystem automation stack, including the LLM planner, agent framework, tool adapters, orchestration API, and sandboxed execution guardrails.

## Components

### 1. LLM Planner (`backend/src/core/llm.py`)
- Provides a provider-agnostic interface for generating automation plans.
- Supports a local stub planner by default.
- Can be configured to use OpenAI via `LLM_API_KEY` and `provider=openai`.
- Produces structured plans with actions, tools, and arguments.

### 2. Agent Framework (`backend/src/core/agent.py`)
- Represents execution endpoints for local or remote nodes.
- For local operation, agents use the `ToolAdapter` to invoke safe tools.
- Remote agents send steps to a node endpoint over HTTP.

### 3. Tool Adapters (`backend/src/core/tool_adapter.py`)
- Provides a registry of safe tool integrations.
- Includes built-in tools:
  - `run_shell` — safe shell execution via sandbox
  - `query_sqlite` — inspect local SQLite databases
  - `list_files` — list directory contents
- Enables reliable tool integration and future extension.

### 4. Orchestration API (`backend/src/api/automation.py`)
- Exposes endpoints for:
  - `/api/automation/run` — execute a goal-driven automation workflow
  - `/api/automation/plan` — generate a plan from a goal
  - `/api/automation/tools` — list available tool adapters
- Integrates with `BornSystem` to manage planning, policy, and execution.

### 5. Safe Execution Sandbox (`backend/src/core/sandbox.py`)
- Validates shell commands before execution.
- Rejects dangerous patterns such as `rm -rf`, `shutdown`, `mkfs`, `sudo`, and command chaining.
- Restricts execution to allowed commands and sandbox directory boundaries.

## Guardrails and Policy Enforcement

### Policy Engine (`backend/src/core/policy.py`)
- Validates plan structure.
- Allows only safe actions: `analyze`, `execute`, `scan`, `report`.
- Rejects forbidden target patterns like `rm -rf`, `shutdown`, `format`, and `drop table`.

### Operational Security

- All local shell execution is sandboxed.
- The automation stack separates planning, tool selection, and execution.
- Remote nodes are invoked only through explicit agent endpoints.
- Tool adapters are registered centrally and can be audited.

## Endpoint Summary

- `GET /api/automation/tools`
- `POST /api/automation/plan`
- `POST /api/automation/run`

## Notes

The new automation stack is intentionally modular and extendable.
Future improvements can add:
- additional tool adapters for RF, camera, and firmware analysis
- real LLM providers beyond the default local stub
- richer node and execution session management
