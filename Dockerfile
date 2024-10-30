FROM python:3.13-slim

ENV SENTRY_PYTHON_DSN=""

RUN apt-get update && apt-get install -y gcc musl-dev cargo libpq5 && mkdir /app

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get autoremove -y gcc musl-dev cargo libpq5

COPY . .

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
