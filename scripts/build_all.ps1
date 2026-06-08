# Build all Docker images for BornSystem
Set-Location -Path "$(Split-Path -Parent $MyInvocation.MyCommand.Path)"
cd ..\

docker compose -f docker\docker-compose.yml build
