#!/bin/bash

# Push changes to DB
# https://www.prisma.io/docs/orm/prisma-migrate/workflows/prototyping-your-schema#choosing-db-push-or-prisma-migrate
prisma db push

# remove "--reload" in production because uvicorn will ignore the "--workers" argument then
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --workers 4