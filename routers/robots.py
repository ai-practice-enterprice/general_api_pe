import logging
import random
from fastapi import APIRouter, Query
from typing import Annotated

from config import DB_CLIENT
from database.db_schema import *

# API endpoints setup ==========================================================================
router = APIRouter(prefix="/robot", tags=["Robots"])
log = logging.getLogger(__name__)


@router.get("/action/direct_control", response_model=str)
def get_control_robot(
    namespace: Annotated[str, Query()] = "jetracer_1",
    message: Annotated[str, Query()] = "{linear: {x: 5.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: -0.1}}",
    topic: Annotated[str, Query()] = "/diff_drive_controller/cmd_vel geometry_msgs/msg/TwistStamped",
):
    """
    Control robot with given message , namespace , topic
    """

@router.get("/action/navigation", response_model=str)
def get_send_nav2_msg(
    namespace: Annotated[str, Query()] = "jetracer_1",
    warehouseZone: Annotated[str, Query()] = "robot_station",
):
    """
    Order robot to go given zone location with given namespace and given zone name
    """


@router.get("/register", response_model=str)
def get_add_robot_to_db(
    namespace: Annotated[str, Query()] = "jetracer_1",
    robottype: Annotated[str, Query()] = "jetracer",
    location: Annotated[str, Query()] = "robot_station",
):
    """
    Add a robot to the database and give it's current location
    """
    newRobot = Robots(
        robotStatus=True,
        robotType=robottype,
        robotNamespace=namespace,
    ) 

    resultQuery = DB_CLIENT.robots.create(newRobot)

    return resultQuery

@router.get("/watch", response_model=str)
def get_all_robot_status():
    """
    Fetch all the robots that are active
    """

    resultQuery = DB_CLIENT.robots.find_many(
        where={
            'robotStatus' : True
        }
    )

    return resultQuery

@router.get("/activate", response_model=str)
def get_set_robot_inactive(
    namespace: Annotated[str, Query()] = "jetracer_1",
    location: Annotated[str, Query()] = "robot_station",
):
    """
    Set a robot as unactive
    """
    resultQuery = DB_CLIENT.robots.update(
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
    Set a robot as active
    """
    resultQuery = DB_CLIENT.robots.update(
        where={
            'robotNamespace': namespace
        },
        data={
            'robotStatus' : True
        }
    )

    return resultQuery



