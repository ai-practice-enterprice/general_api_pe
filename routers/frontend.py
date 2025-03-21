import logging
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel, Field
from prisma.models import Robots
from typing import Annotated


router = APIRouter(prefix="/frontend", tags=["Frontend"])
log = logging.getLogger(__name__)


class RobotCreationRequest(BaseModel):
    robot_type: str = Field(alias="robotType")
    robot_namespace: str = Field(alias="robotNamespace")
    robot_status: bool = Field(alias="robotStatus")


@router.post("/robot")
async def create_robot(robot: RobotCreationRequest):
    """
    Create a new robot
    """
    log.info(f"Creating a new robot: {robot.robot_namespace} of type {robot.robot_type}")
    await Robots.prisma().create({
        "robotNamespace": robot.robot_namespace,
        "robotType": robot.robot_type,
        "robotStatus": robot.robot_status
    })

    return {"status": "success"}


@router.get("/robot/all")
async def read_robots():
    """
    Fetch all robots
    """
    robots = await Robots.prisma().find_many()
    return robots


@router.patch("/robot/{robot_id}/toggle")
async def update_robot(robot_id: int):
    """
    Update the status of a robot
    """
    robot = await Robots.prisma().find_unique(where={"robotID": robot_id})
    if not robot:
        raise HTTPException(status_code=404, detail="Robot not found")

    new_status = not robot.robotStatus
    await Robots.prisma().update(where={"robotID": robot_id}, data={"robotStatus": new_status})

    return {"status": "success"}
