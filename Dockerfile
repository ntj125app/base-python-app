FROM python:3.13-slim

ENV SENTRY_PYTHON_DSN=""

COPY requirements.txt ./

RUN apt-get update && apt-get install -y gcc musl-dev cargo libpq5 && mkdir /app  && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get autoremove -y gcc musl-dev cargo libpq5 && \
    apt-get autoclean -y

WORKDIR /app

COPY . .

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
