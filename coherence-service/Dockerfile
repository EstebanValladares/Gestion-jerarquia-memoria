FROM python:3.10-slim

WORKDIR /app

RUN pip install Flask

COPY coherence_server.py .

CMD ["python", "coherence_server.py"]