FROM python:3.11-slim

WORKDIR /app

COPY src/ ./src/
COPY data/ ./data/
COPY run.py .

CMD ["python", "run.py"]
