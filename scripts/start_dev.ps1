# Start the full BornSystem stack for development
Set-Location -Path "$(Split-Path -Parent $MyInvocation.MyCommand.Path)"
cd ..\
docker compose -f docker\docker-compose.yml up --build
