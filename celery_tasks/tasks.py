from prisma.models import Robots, Paths, Zones , PackageMovement , Packages , OrderMovement

import logging
import random

import asyncio
from arq import create_pool, ArqRedis, cron
from arq.connections import RedisSettings
from arq.jobs import Job

log = logging.getLogger(__name__)

# about retries:
# https://docs.celeryq.dev/en/latest/userguide/tasks.html#bound-tasks
# https://testdriven.io/blog/retrying-failed-celery-tasks/
# https://en.wikipedia.org/wiki/Exponential_backoff
# https://stackoverflow.com/questions/6499952/recover-from-task-failed-beyond-max-retries
# https://github.com/celery/celery/issues/5061


# create the taskqueue functions ===========================================================
def process_order(zone_id: int, package_id: int):
    log.info(f"Attempting to clear package {package_id} from zone {zone_id}...")

    # 1) Find an available robot
    # 1.1) Exception handeling if no robot available => retry +1
    robots = Robots.prisma().find_many(where={"robotStatus" : True})
    if len(robots) == 0: 
        raise Exception()
    else :
        r1 = random.choices(robots)
    
    # Lorenzo => 
    # 1.2) Exception handeling if no robot available => retry == max_retries
    
    # 1.2.1) Exception handeling of no robot available => Query DB to verify 
    # 1.2.1.1) Query does not work after 4 query tries ? => Distress call => proceed to full shutdown
    # 1.2.1.2) Confirmation all robots busy ? => Distress call => proceed to normal shutdown

    # full shutdown => all zones are set to False + Error on dashboard should be displayed that DB is down
    # normal shutdown => all zones are set to False

    # 2) from the robots use either manhattan distance as a metric or just random.choices (with or without weights)
    
    # 3) use httpx to send a htttp request using the GET method for the bsu-ros-server (see docker-compose) to handle and then send to the RosApiBridge


async def check_for_package_to_move(ctx: dict):
    redis = await create_pool(RedisSettings())
    log.info("arq: Checking for packages to move")
    session = ctx['prisma']
    try:
        new_orders = await PackageMovement.prisma().find_many(
            where={
                "zones": {
                    "is": {
                        "zoneType": "DropZoneIn"
                    }
                }
            },
            include={"zones": True, "packages": True}
        )
        log.info(f"arq: Found {len(new_orders)} new orders.")
        for pm in new_orders:
            await redis.enqueue_job('process_order',zone_id = pm["ZoneID"],package_id = pm["PackageID"])
    except Exception as e:
        log.error(f"arq: Error checking for new orders: {e}")

# create the taskqueue functions ===========================================================

