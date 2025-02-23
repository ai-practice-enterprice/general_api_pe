import os
import pkgutil
import importlib
import logging
from logging.handlers import TimedRotatingFileHandler
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from typing import AsyncIterator

load_dotenv(override=os.getenv("OVERRIDE_SYSTEM") == "true")

import routers


@asynccontextmanager
async def lifespan(_) -> AsyncIterator[None]:
    log.info("Starting up")
    yield
    log.info("Shutting down")


# Create main app
app = FastAPI(lifespan=lifespan)

# Set up logging
log = logging.getLogger(__package__)
log.setLevel(logging.INFO)

# Ensure the logs directory exists
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Set up log handlers and formatters
formatter = logging.Formatter(
    '%(levelname)s:%(asctime)s:%(name)s:%(message)s'
)

file_handler = TimedRotatingFileHandler(
    os.path.join(log_dir, 'info.log'),
    when='midnight',
    interval=1,
    backupCount=10
)
file_handler.setFormatter(formatter)
log.addHandler(file_handler)

# Add a stream handler for console output
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
log.addHandler(stream_handler)

# Register all routers
for module_info in pkgutil.iter_modules(routers.__path__):
    module = importlib.import_module(f'routers.{module_info.name}')
    if hasattr(module, "router"):
        log.info(f"Registering routes from {module_info.name}")
        app.include_router(module.router)
