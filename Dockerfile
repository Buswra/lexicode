FROM python:3.12-slim

WORKDIR /app

COPY requirements-web.txt .
RUN pip install --no-cache-dir -r requirements-web.txt

COPY features/ ./features/

CMD gunicorn features.app:app --bind 0.0.0.0:$PORT
