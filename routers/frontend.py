import logging
import os
import random
import pprint
import httpx
from enum import Enum

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import prisma
from celery_tasks import tasks
from prisma.models import Robots, Paths, Zones , PackageMovement , Packages , OrderMovement
from typing import Annotated, List
from faker import Faker

from map_gen.MapPlotter import MapPlotter 
from map_gen.config import WIDTH , HEIGHT , TILE_SIZE


router = APIRouter(prefix="/frontend", tags=["Frontend"])
log = logging.getLogger(__name__)

# ======================== API fake AD team DATABASE ======================== #


# THIS IS A TEMP FUNC SO CHANGES ARE ALLOWED TO INCREASE REALASTIC BEHAVIOUR (such as: DB conn failed , courrier missing , no data fetched , etc...)
def fetch_fake_remote_packagedata_from_AD_team(courrier_id: int,courrier_max_id: int = 10):

    # 1% chance of error
    if random.randint(1,1000) == 1:
        raise Exception("Could not connect...")

    # courier does not exist
    if courrier_id not in range(1,courrier_max_id + 1):
        raise Exception("Courrier does not exist...")

    # other errors that you might think of that could break our server
    # ...
    #  ...

    data: list[dict] = []
    fake = Faker()
    for x in range(1,500):
        data.append({
            "packageID"    : x,
            "courrierID"   : random.randint(1,courrier_max_id),
            "streetName"   : fake.street_name(),
            "houseNumber"  : str(random.randint(1,300)),
            "cityName"     : fake.city(),
            "cityPostcode" : fake.postcode(),            
        }) 

    fetched_data: list[dict] = []
    for package in data:
        if package["courrierID"] == courrier_id: 
            fetched_data.append(package)
    
    return fetched_data

# ======================== models for API request (NOT for database => see schema.prisma) ======================== #

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

class PathCreationRequest(BaseModel):
    path_number: int = Field(alias="pathNumber")
    path_description: str = Field(alias="pathDescription")
    path_zone_start: int = Field(alias="pathZoneStart")
    path_zone_end: int = Field(alias="pathZoneEnd")
    path_coordinates: List[List[float]] = Field(alias="pathCoordinates")
    path_active: bool = Field(alias="pathActive")


# ======================== API endpoints for robot data ======================== #
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
    log.info(f"{robots}")
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






# ======================== API endpoints for zone data ======================== #
@router.get("/zone/all")
async def read_zones():
    """
    Fetch all zones
    """
    zones = await Zones.prisma().find_many()
    return zones

@router.get("/zone/all", response_model=list[Zones])
async def read_zones_of_type(
    zone_type: Annotated[str, Query()] = "DropZoneIn"
):
    """
    Fetch all zone of certain type (e.g.: RobotStation , DropZoneIn , ErrorZone)
    """
    zones = await Zones.prisma().find_many(where={"zoneType" : zone_type})
    return zones

@router.patch("/zone/data/{zone_id}")
async def read_single_zone(
    zone_id: int
):
    """
    Fetch data of 1 zone
    """
    zone = await Zones.prisma().find_unique(where={"zoneID" : zone_id})
    return zone

@router.post("/zone/map_warehouse",responses={200 : {"content": {"image/xml+svg": {}},}})
async def get_map_warehouse():
    """
    Fetch the warehouses interactive map base upon MapPlotter
    """
    path_to_map = os.path.join(
        os.path.dirname(__file__),
        "..",
        "map_gen",
        "map.svg"
    )

    mp = MapPlotter(mode="SVG",tilesize=TILE_SIZE,size=(WIDTH,HEIGHT),filename=path_to_map)
    mp.draw_tiles()
    mp.draw_connections()
    mp.draw_centers()
    mp.save_map()


    return FileResponse(path=path_to_map)


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


@router.patch("/zone/{zone_id}/enter")
async def enter_zone(zone_id: int,courrier_id: int = 1):
    """
    Mark a zone as entered
    """
    # ealry fails to prevent the worker from entering a unavailable zone
    zone = await Zones.prisma().find_unique(where={"zoneID": zone_id})
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    if not zone.zoneAvailable:
        raise HTTPException(status_code=400, detail="Zone is not available")
    

    # --- !!! NEEDS TO BE REPLACED WITH ACTUAL URL and COURRIER ID !!! --- #
    try:
        # REAL
        # packages_fetched = httpx.get(url=f"http://bsu-ad-server/courriers?courrierID={courrier_id}")

        # FAKE
        courrier_id = 1
        packages_fetched = fetch_fake_remote_packagedata_from_AD_team(courrier_id)

    except Exception as e:
        log.info(f"AD Server unresponsive. Please try again later... \n arguments => {e.args}")
        raise HTTPException(status_code=500, detail="AD Server unresponsive")
    
    # --- !!! NEEDS TO BE REPLACED WITH ACTUAL URL and COURRIER ID !!! --- #

    # 1) here we create the data (might not be necessary but we might also get back some fields that we don't require)
    # that is tailored for our dataabase
    insert_data_package = []
    insert_data_packageMov = []
    for package in packages_fetched:
        insert_data_package.append({
            "packageID" : package["packageID"],
            "streetName" : package["streetName"], 
            "houseNumber" : package["houseNumber"], 
            "cityName" : package["cityName"], 
            "cityPostcode" : package["cityPostcode"], 
        })

        insert_data_packageMov.append({
            "ZoneID" : zone_id,
            "PackageID" : package["packageID"],
        })
    
    try:

        # 2) here we add the packages to the DB
        await Packages.prisma().create_many(
            data=insert_data_package
        )

        # 3) here we add the packages about WHERE they are inside the warehouse (hopefully) to the DB
        await PackageMovement.prisma().create_many(
            data=insert_data_packageMov
        )

    except Exception as e:
        log.info(f"AI Server encountered some error when trying to insert the fetched data {e}")
        raise HTTPException(status_code=500, detail="AI Server encountered some error when trying to insert the fetched data")

    try:

        # 4) here we update the zone
        await Zones.prisma().update(where={"zoneID": zone_id}, data={"zoneAvailable": False})
    
    except Exception as e:
        log.info(f"AI Server encountered some error when trying to update the zone {e}")
        raise HTTPException(status_code=500, detail="AI Server encountered some error when trying to update the zone")

    return {"status": "success"}


@router.patch("/zone/{zone_id}/exit")
async def exit_zone(zone_id: int):
    """
    Mark a zone as exited
    """
    zone = await Zones.prisma().find_unique(where={"zoneID": zone_id})
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    if not zone.zoneAvailable:
        raise HTTPException(status_code=400, detail="Zone is not available")

    await Zones.prisma().update(where={"zoneID": zone_id}, data={"zoneAvailable": False})

    return {"status": "success"}






# ======================== API endpoints for path data ======================== #
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
