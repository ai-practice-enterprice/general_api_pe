#!/bin/bash

# https://prisma-client-py.readthedocs.io/en/stable/getting_started/quickstart/
# The db push command also generates the client for you. 
# If you want to generate the client without modifying your database, use the following command: prisma generate --watch
# remove "--reload" in production because uvicorn will ignore the "--workers" argument then

set -e  
prisma db push
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --workers 4