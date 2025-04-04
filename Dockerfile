FROM python:3.12-slim AS builder
WORKDIR /app

# we install nodejs so that we can run prisma studio (a GUI) for having interface to the DB
RUN apt-get update && apt-get install -y \
    libzbar0 \
    nodejs \
    npm && \
    rm -rf /var/lib/apt/lists/*

COPY . .
RUN chmod 777 ./entrypoint.sh
RUN pip install --no-cache-dir -r requirements.txt

# https://prisma-client-py.readthedocs.io/en/stable/getting_started/quickstart/
# The db push command also generates the client for you. 
# If you want to generate the client without modifying your database, use the following command: prisma generate --watch

ENV DATABASE_URL=mysql://aiUser:pwdAIteamDB@bsu-db-server:3306/bsu_warehouse_db
# Generate Prisma client
RUN prisma generate

EXPOSE 8000

CMD ["/bin/sh","entrypoint.sh" ]
