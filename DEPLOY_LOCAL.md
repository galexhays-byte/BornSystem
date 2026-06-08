# Local Deployment Guide

This guide describes how to deploy BornSystem locally for testing and development.

## Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for development)
- 2GB RAM minimum, 4GB recommended

## Quick Start

### 1. Clone and Navigate
```bash
cd c:\idea\BornSystem\BornSystem
```

### 2. Set Environment (Optional)
```bash
cp .env.example .env
# Edit .env if you need to enable OpenAI LLM support
```

### 3. Build and Run
```bash
docker-compose -f docker/docker-compose.yml up -d
```

### 4. Verify Services
- Backend health: `http://localhost:8000/health`
- Frontend UI: `http://localhost:3000`
- Kali node: `http://localhost:8001`
- Ubuntu node: `http://localhost:8002`

## Testing the Automation API

### 1. List available automation tools
```bash
curl http://localhost:8000/api/automation/tools
```

### 2. Generate a plan for a goal
```bash
curl -X POST http://localhost:8000/api/automation/plan \
  -H "Content-Type: application/json" \
  -d '{"goal": "scan network for cameras on 192.168.1.1/24"}'
```

### 3. Run an automation workflow
```bash
curl -X POST http://localhost:8000/api/automation/run \
  -H "Content-Type: application/json" \
  -d '{"goal": "discover cameras on 192.168.1.0/24"}'
```

### 4. Execute a workflow via API
```bash
curl -X POST http://localhost:8000/api/workflows/execute \
  -H "Content-Type: application/json" \
  -d '{"workflow_id": "camera_discovery", "target": "192.168.1.0/24"}'
```

## Frontend Testing

Open `http://localhost:3000` in a browser and use the UI controls:
- **Check backend health** — verify backend is running
- **List automation tools** — see available tool adapters
- **Generate automation plan** — plan a goal-driven workflow
- **Run automation** — execute a goal-driven automation

## Stopping Services
```bash
docker-compose -f docker/docker-compose.yml down
```

## Local Development (Without Docker)

If running without Docker, ensure your Python environment has the required dependencies installed:

```bash
pip install fastapi uvicorn pydantic
python backend/src/main.py
```

The API will be available at `http://localhost:8000`.

## Troubleshooting

- **Port conflicts**: Change port mappings in `docker/docker-compose.yml`
- **Database not found**: Run `python database/init_db.py` to initialize the threat DB
- **Tool execution fails**: Ensure nmap and other tools are installed in node containers
- **No automation output**: Check `LLM_API_KEY` is set for full LLM integration, or use the default stub planner
