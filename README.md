# BornSystem

BornSystem is the master AI automation platform for your project.
It contains a production-ready repository layout for:
- backend API core
- frontend UI
- node execution agents
- Docker orchestration
- automation scripts
- documentation and workflow templates

## Getting started

1. Open `c:\idea\BornSystem\BornSystem`
2. Build the backend:
   - `cd backend`
   - `pip install -r requirements.txt`
3. Start the full system with Docker Compose:
   - `docker compose -f docker/docker-compose.yml up --build`
4. Open these endpoints:
   - Backend API: `http://localhost:8000/health`
   - Frontend: `http://localhost:3000`

## Structure

- `/backend` — FastAPI orchestration core
- `/frontend` — static UI assets and front-end shell
- `/nodes` — node containers for Kali, Ubuntu, and Windows agents
- `/docker` — compose definition and image build files
- `/cloud-server` — MinIO and PostgreSQL stack for cloud-ready object storage and metadata
- `/storage` — binaries, scripts, configs, and logs for field devices
- `/database` — SQLite schema and initialization for threat data
- `/scripts` — helper launch and build scripts
- `/docs` — architecture and developer documentation
- `/workflows` — CI/workflow templates

## Ubuntu home deployment

This project is designed to run on a local Ubuntu server first, with paths for future cloud migration.
The `cloud-server/` stack can be moved into a hosted Ubuntu instance later.
