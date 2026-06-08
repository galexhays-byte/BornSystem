# BornSystem Backend

The backend handles all system logic, APIs, authentication, orchestration, and communication between nodes.

## Responsibilities

- Core API endpoints
- Node orchestration and execution
- Policy and safety enforcement
- Runtime state management
- FastAPI-based service layer
- Tool and workflow integration

## Current Structure

- `requirements.txt` — Python dependencies
- `Dockerfile` — backend Python container
- `/src/main.py` — FastAPI entrypoint
- `/src/api/` — REST endpoint modules
- `/src/core/` — orchestration and node management

## Notes

The current production scaffold uses the `/src` package inside backend for the core BornSystem backend implementation.
