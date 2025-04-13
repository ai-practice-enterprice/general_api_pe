import os
import pkgutil
import importlib
import routers
import asyncio
import threading
from typing import AsyncIterator, Annotated
from dotenv import load_dotenv

from contextlib import asynccontextmanager

from celery import Celery
from prisma import Prisma

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import logging
from logging.handlers import TimedRotatingFileHandler

# contains all URL configurations 
from config import ORIGINS , CELERY_BROKER_URL , CELERY_RESULT_BACKEND

# contains all functions to generate fake DB
from database.push_data import push_fake_data_to_db

from map_gen.config import MAP
 
# loads env variables (can be implemented or said later on to increase security (such as passwords and other env variables))
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
    # add fake data to DB =====================================================
    await push_fake_data_to_db(
        push_packages = True,
        push_zones = True,
        push_robots = True,
        push_paths = True,
        number_of_records = {
            "packages_rec_nbr"  : 100,
            "zones_map"         : MAP,
            "robots_rec_nbr"    : 5,
        }
    )
    # add fake data to DB =====================================================

    yield
    log.info("Shutting down")
    await prisma.disconnect()

# Create main app ===================================================== 
app = FastAPI(lifespan=lifespan)

# add the CORS for allowing other application to talk to the API server
# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    # instead of all (*) for security use => ORIGINS from the config file
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://geshan.com.np/blog/2022/01/redis-docker/
# https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html
# https://derlin.github.io/introduction-to-fastapi-and-celery/03-celery/
celery_app = Celery(
    main=__name__, 
    broker=CELERY_BROKER_URL, 
    backend=CELERY_RESULT_BACKEND,
    include=['celery_tasks.tasks'],
)


# https://lip17.medium.com/hands-on-learn-python-celery-in-30-minutes-9544aabb70b1
# https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html
celery_app.conf.update(
    beat_schedule={
            'check-task-queue': {
            'task': 'celery_tasks.tasks.check_for_package_to_move',
            'schedule': 10.0, # run every 60 seconds 
            # => so when new packages comes in and are added to the DB. 
            # The packages won't be handled until the next cycle starts 
        },
    }
)

# (1) -> tasks are functions in Celery, the units of work are defined as Python functions decorated with @celery_app.task (or anything else)
# (2) -> you add work to the Celery queue by calling the:
#    .delay() method 
#    or .send_task()) on your Celery task function.
#    adding it to the beat function 
# This serializes the task's arguments and sends a message to the Celery broker 
# (like Redis or RabbitMQ).
# (3) -> workers consume tasks by listing to the broker and pick up these task messages 
# to execute the corresponding Python function.

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

