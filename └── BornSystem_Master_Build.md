# BornSystem Master Build
# BornSystem — Master Build File

This file defines the entire BornSystem architecture.
It is the single source of truth for the BornSystem project structure.

## 1. Project Structure (Top Level)

The BornSystem project contains the following top-level directories:

- `/backend` — fastapi orchestration core and API
- `/frontend` — static UI shell, CSS, and client scripts
- `/nodes` — containerized node agents for Kali, Ubuntu, and Windows
- `/docker` — multi-container orchestration and Docker build files
- `/cloud-server` — object storage and metadata engine for hosted Ubuntu servers
- `/storage` — binaries, scripts, configs, and logs for field deployments
- `/database` — threat database schema, initialization, and local storage assets
- `/scripts` — developer launch, build, and deployment scripts
- `/tools` — curated tool repositories for Linux, Windows, and custom agents
- `/workflows` — workflow templates for recon, scanning, exploitation, and reporting
- `/docs` — architecture, API, node, and workflow documentation

## 2. Backend Architecture

`/backend`
- `requirements.txt` — Python dependencies for the backend
- `Dockerfile` — container build file for the Python API service
- `/src`
  - `main.py` — FastAPI entrypoint and route registration
  - `/api`
    - `example.py` — sample endpoint
    - `system.py` — system metadata and health routes
    - `nodes.py` — node orchestration endpoints
  - `/core`
    - `orchestrator.py` — planning, scheduling, and dispatch logic
    - `node_registry.py` — node registration and selection
    - `agent.py` — execution agent abstraction
    - `policy.py` — policy guardrails and validation
    - `state_manager.py` — runtime state persistence

## 3. Frontend Architecture

`/frontend`
- `package.json` — frontend package config and run script
- `Dockerfile` — static website container build
- `/public`
  - `index.html` — UI shell
- `/css`
  - `style.css` — interface styling
- `/js`
  - `app.js` — frontend interaction and API calls

## 4. Nodes Architecture

`/nodes`
- `kali/` — Kali Linux node container and agent
  - `Dockerfile`
  - `/agent/agent.py`
- `ubuntu/` — Ubuntu node container and agent
  - `Dockerfile`
  - `/agent/agent.py`
- `windows/` — Windows agent placeholder
  - `/agent/agent.py`

## 5. Cloud Server Architecture

`/cloud-server`
- `docker-compose.yml` — MinIO + PostgreSQL stack for Ubuntu and cloud deployment
- `README.md` — deployment guidance for home or cloud environments
- `.env.example` — sample credentials for object store and database services

## 6. Storage & Threat Data

`/storage`
- `README.md` — storage layout and usage
- `/binaries` — runtime binaries for field devices
- `/scripts` — field automation scripts
- `/configs` — signature datasets and scan payloads
- `/logs` — captured output and local logs

`/database`
- `schema.sql` — SQLite schema for RF signals, firmware fingerprints, and discovery logs
- `README.md` — database design and usage
- `init_db.py` — database initialization script

## 7. Docker Orchestration

`/docker`
- `docker-compose.yml` — local full-stack orchestration
- `backend.Dockerfile` — backend service build definition
- `frontend.Dockerfile` — frontend service build definition
- `kali-node.Dockerfile` — Kali node build definition
- `ubuntu-node.Dockerfile` — Ubuntu node build definition

## 6. Developer Scripts

`/scripts`
- `build_all.ps1` — build all Docker images
- `start_dev.ps1` — launch the full stack in development mode

## 7. Workflows and CI Templates

`/workflows`
- `recon/recon.yml`
- `scanning/scanning.yml`
- `exploitation/exploitation.yml`
- `reporting/reporting.yml`

## 8. Documentation

`/docs`
- `architecture/README.md` — system architecture overview
- `api/README.md` — API endpoint documentation
- `nodes/README.md` — node agent documentation
- `workflows/README.md` — workflow definitions and usage

## 9. Recommended Launch Sequence

1. Install backend dependencies:
   - `cd backend`
   - `pip install -r requirements.txt`
2. Install frontend dependencies:
   - `cd frontend`
   - `npm install`
3. Start the platform:
   - `cd ..`
   - `docker compose -f docker/docker-compose.yml up --build`
4. Verify endpoints:
   - `http://localhost:8000/health`
   - `http://localhost:3000`

## 10. Production Readiness Notes

- The backend is ready for expansion with real planning, node orchestration, and policy enforcement.
- The frontend is a minimal dashboard shell with live API integration.
- Node containers are scaffolded and can be extended with Kali/Ubuntu tooling.
- The Docker compose stack connects backend, frontend, and node services for local validation.
