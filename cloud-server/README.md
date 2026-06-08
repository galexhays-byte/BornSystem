# BornSystem Cloud Server Stack

This folder contains the Docker stack for the future cloud-hosted BornSystem backend.
It is built to run on Ubuntu first as a local home server and then migrate to a hosted cloud instance.

## Services

- `minio` — S3-compatible object storage for binaries, scripts, configurations, and logs
- `postgres-db` — metadata database for jobs, hosts, and system state

## Run locally

From this folder:

```bash
docker compose up -d
```

## Environment

Use `cloud-server/.env.example` to configure service credentials before deployment.
