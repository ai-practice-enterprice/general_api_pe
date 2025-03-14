FROM python:3.12-slim AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libzbar0 \
    nodejs \
    npm && \
    rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

RUN chmod +x ./entrypoint.sh
CMD ["./entrypoint.sh"]
