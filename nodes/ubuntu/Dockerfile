FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn
COPY agent ./agent
EXPOSE 8001
CMD ["uvicorn", "agent.agent:app", "--host", "0.0.0.0", "--port", "8001"]
