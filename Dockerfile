FROM python:3.12-slim AS builder
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
RUN chmod +x ./entrypoint.sh
CMD ["./entrypoint.sh"]
