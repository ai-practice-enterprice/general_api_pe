import logging
from fastapi import APIRouter, Query
from typing import Annotated
import httpx

# Import database client and models
from database.db_schema import Robots as RobotsSchema
from prisma.models import Robots


# Setup API router
router = APIRouter(prefix="/robot", tags=["Robots"])
log = logging.getLogger(__name__)



# ======================== Robot Control Endpoints ========================

@router.get("/action/direct_control", response_model=str)
def get_control_robot(
    namespace: Annotated[str, Query()] = "jetracer_1",
    message: Annotated[str, Query()] = "{linear: {x: 5.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: -0.1}}",
    topic: Annotated[str, Query()] = "/diff_drive_controller/cmd_vel",
):
    """
    Directly control a robot by sending a movement command.
    - `namespace`: The identifier for the robot.
    - `message`: The control message containing movement parameters.
    - `topic`: The topic where the command should be sent.
    """


@router.get("/action/navigation", response_model=str)
def get_send_nav2_msg(
    namespace: Annotated[str, Query()] = "jetracer_1",
    warehouseZone: Annotated[str, Query()] = "robot_station",
):
    """
    Send a robot to a specific zone in the warehouse.
    - `namespace`: The identifier for the robot.
    - `warehouseZone`: The target location for the robot.
    """



# ======================== Robot Database Management ========================

@router.get("/register", response_model=str)
def get_add_robot_to_db(
    namespace: Annotated[str, Query()] = "jetracer_1",
    robottype: Annotated[str, Query()] = "jetracer",
    location: Annotated[str, Query()] = "robot_station",
):
    """
    Register a new robot in the database with its initial location.
    - `namespace`: Unique identifier for the robot.
    - `robottype`: Type of the robot.
    - `location`: Initial warehouse location of the robot.
    """
    newRobot = RobotsSchema(
        robotStatus=True, #status = active
        robotType=robottype,
        robotNamespace=namespace,
    ) 

    resultQuery = Robots.prisma().create(data=newRobot.model_dump())
    return resultQuery


@router.get("/watch", response_model=str)
def get_all_robot_status():
    """
    Retrieve a list of all active robots from the database.
    """

    resultQuery = Robots.prisma().find_many(
        where={
            'robotStatus' : True
        }
    )

    return resultQuery


# ======================== Robot Status Management ========================

@router.get("/activate", response_model=str)
def get_set_robot_inactive(
    namespace: Annotated[str, Query()] = "jetracer_1",
    location: Annotated[str, Query()] = "robot_station",
):
    """
    Set a robot as inactive in the database.
    - `namespace`: Unique identifier for the robot.
    - `location`: Current location of the robot (not used in update but provided for clarity).
    """
    resultQuery = Robots.prisma().update_many(
        where={
            'robotNamespace': namespace
        },
        data={
            'robotStatus' : False
        }
    )

    return resultQuery


@router.get("/deactivate", response_model=str)
def get_set_robot_active(
    namespace: Annotated[str, Query()] = "jetracer_1",
):
    """
    Set a robot as active (enabled) in the database.
    - `namespace`: Unique identifier for the robot.
    """
    resultQuery = Robots.prisma().update_many(
        where={
            'robotNamespace': namespace
        },
        data={
            'robotStatus' : True
        }
    )

    return resultQuery
