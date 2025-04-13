#!/bin/bash

# https://prisma-client-py.readthedocs.io/en/stable/getting_started/quickstart/
# The db push command also generates the client for you. 
# If you want to generate the client without modifying your database, use the following command: prisma generate --watch
# Generate Prisma client
prisma generate
# Push changes to DB
# https://www.prisma.io/docs/orm/prisma-migrate/workflows/prototyping-your-schema#choosing-db-push-or-prisma-migrate
prisma db push

# https://www.linkedin.com/pulse/setting-up-celery-your-django-project-ubuntu-server-akshay-kaushik-t7r9c
# https://lip17.medium.com/hands-on-learn-python-celery-in-30-minutes-9544aabb70b1
# to see options use : celery --help
# or : celery worker --help
# or : celery beat --help
celery --app=main.celery_app worker --loglevel=INFO &
celery --app=main.celery_app beat --loglevel=INFO &
# remove "--reload" in production because uvicorn will ignore the "--workers" argument then
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --workers 4
