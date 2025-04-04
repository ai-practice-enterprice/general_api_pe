import os
import pkgutil
import importlib
import routers
from typing import AsyncIterator, Annotated
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from prisma import Prisma
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from logging.handlers import TimedRotatingFileHandler

# contains all URL configurations 
from config import ORIGINS
 
# loads env variables (ask Lorenzo why neccessary)
load_dotenv(override=True)


# FastAPI (https://realpython.com/fastapi-python-web-apis/)
# uses events or a lifespan parameter to handle it's runtime logic before booting and after shutdown
# however you must choose between the 2. as stated in the docs "It's all lifespan or all events, not both."
# https://fastapi.tiangolo.com/advanced/events/#async-context-manager  
@asynccontextmanager
async def lifespan(_) -> AsyncIterator[None]:
    # Prisma requires a client. The client is a auto-generated and type-safe query builder that's tailored to your data. (as stated in the docs : https://www.prisma.io/docs/orm/prisma-client/setup-and-configuration/introduction)
    # the Prisma client requires a schema file (usually : schema.prisma) which is a file that defines: 
    # - the "models" (tables in your DB) , 
    # - your datasource (your URL where your DB is located)
    # - and your generator (which is your DB provider) 
    # Once the prisma file is made and Prisma is INSTALLED you  can run "prisma generate" in the root of the directory 
    # You can also run "prisma studio" which offers a GUI to the database for developement
    prisma = Prisma(auto_register=True)
    log.info("Starting up")
    await prisma.connect()
    yield
    log.info("Shutting down")
    await prisma.disconnect()

# Create main app ===================================================== 
app = FastAPI(lifespan=lifespan)

# add the CORS for allowing other application to talk to the API server
# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Create main app ===================================================== 



# Set up logging =====================================================
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
# Set up logging =====================================================



# add routers =====================================================
# Register all submodules of the router module i.e. all routers inside the routers folder
for module_info in pkgutil.iter_modules(routers.__path__):
    module = importlib.import_module(f'routers.{module_info.name}')
    if hasattr(module, "router"):
        log.info(f"Registering routes from {module_info.name}")
        app.include_router(module.router)
# add routers =====================================================