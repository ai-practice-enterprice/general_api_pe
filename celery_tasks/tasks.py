from prisma.models import Robots, Paths, Zones , PackageMovement , Packages , OrderMovement
import logging
import random
from main import celery_app

log = logging.getLogger(__name__)

# about retries:
# https://docs.celeryq.dev/en/latest/userguide/tasks.html#bound-tasks
# https://testdriven.io/blog/retrying-failed-celery-tasks/
# https://en.wikipedia.org/wiki/Exponential_backoff
# https://stackoverflow.com/questions/6499952/recover-from-task-failed-beyond-max-retries
# https://github.com/celery/celery/issues/5061


# create the taskqueue functions ===========================================================
@celery_app.task(bind=True, autoretry_for=(Exception,),retry_backoff=True, retry_kwargs={'max_retries': 3,})
def process_order(self, zone_id: int, package_id: int):
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


@celery_app.task(bind=True)
def check_for_package_to_move(self):
    log.info("Checking for packages to move")
    try:
        # new_orders = PackageMovement.prisma().find_many(
        #     where={
        #         "zones" : {
        #             "is" : {
        #                 "zoneType" : "DropZoneIn"
        #             }
        #         }
        #     },
        #     include={"zones":True,"packages":True}
        # )
        # log.info(f"Found {len(new_orders)} new orders.")
        log.info(f"Fetched 0 new orders.")
        # # pm == PackageMovement
        # for pm in new_orders:
        #     process_order.delay(pm["ZoneID"],pm["PackageID"])
            
    except Exception as e:
        log.info(f"Error checking for new orders: {e}")

# create the taskqueue functions ===========================================================