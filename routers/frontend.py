import logging
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel, Field
from prisma.models import Robots, Paths, Zones
from typing import Annotated, List


router = APIRouter(prefix="/frontend", tags=["Frontend"])
log = logging.getLogger(__name__)


class RobotCreationRequest(BaseModel):
    robot_type: str = Field(alias="robotType")
    robot_namespace: str = Field(alias="robotNamespace")
    robot_status: bool = Field(alias="robotStatus")


class ZoneCreationRequest(BaseModel):
    zone_name: str = Field(alias="zoneName")
    zone_type: str = Field(alias="zoneType")
    zone_description: str = Field(alias="zoneDescription")
    zone_available: bool = Field(alias="zoneAvailable")
    zone_check: bool = Field(alias="zoneCheck")


class PathCoordinate(BaseModel):
    x: float
    y: float


class PathCreationRequest(BaseModel):
    path_number: int = Field(alias="pathNumber")
    path_description: str = Field(alias="pathDescription")
    path_zone_start: int = Field(alias="pathZoneStart")
    path_zone_end: int = Field(alias="pathZoneEnd")
    path_coordinates: List[List[float]] = Field(alias="pathCoordinates")
    path_active: bool = Field(alias="pathActive")


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


@router.get("/zone/all")
async def read_zones():
    """
    Fetch all zones
    """
    zones = await Zones.prisma().find_many()
    return zones


@router.post("/zone")
async def create_zone(zone: ZoneCreationRequest):
    """
    Create a new zone
    """
    log.info(f"Creating a new zone: {zone.zone_name} of type {zone.zone_type}")
    await Zones.prisma().create({
        "zoneName": zone.zone_name,
        "zoneType": zone.zone_type,
        "zoneDescription": zone.zone_description,
        "zoneAvailable": zone.zone_available,
        "zoneCheck": zone.zone_check
    })
    return {"status": "success"}


@router.patch("/zone/{zone_id}/toggle")
async def toggle_zone_availability(zone_id: int):
    """
    Toggle the availability of a zone
    """
    zone = await Zones.prisma().find_unique(where={"zoneID": zone_id})
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")

    new_availability = not zone.zoneAvailable
    await Zones.prisma().update(where={"zoneID": zone_id}, data={"zoneAvailable": new_availability})

    return {"status": "success"}


@router.get("/path/all")
async def read_paths():
    """
    Fetch all paths with zone information
    """
    paths = await Paths.prisma().find_many(
        include={
            "zoneStart": True,
            "zoneEnd": True
        }
    )
    return paths


@router.post("/path")
async def create_path(path: PathCreationRequest):
    """
    Create a new path
    """
    log.info(f"Creating a new path: {path.path_number} from zone {path.path_zone_start} to {path.path_zone_end}")
    
    # Convert the coordinates to a string for storage
    path_coordinates_str = str(path.path_coordinates)
    
    await Paths.prisma().create({
        "pathNumber": path.path_number,
        "pathDescription": path.path_description,
        "pathZoneStart": path.path_zone_start,
        "pathZoneEnd": path.path_zone_end,
        "pathCoordinates": path_coordinates_str,
        "pathActive": path.path_active
    })
    
    return {"status": "success"}


@router.patch("/path/{path_id}/toggle")
async def toggle_path_status(path_id: int):
    """
    Toggle the active status of a path
    """
    path = await Paths.prisma().find_unique(where={"pathID": path_id})
    if not path:
        raise HTTPException(status_code=404, detail="Path not found")

    new_status = not path.pathActive
    await Paths.prisma().update(where={"pathID": path_id}, data={"pathActive": new_status})

    return {"status": "success"}
