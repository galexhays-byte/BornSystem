FROM ubuntu:24.04
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY agent ./agent
CMD ["python3", "agent/agent.py"]
