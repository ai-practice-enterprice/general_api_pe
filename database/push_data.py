import random
import numpy as np
from datetime import datetime , timedelta
from utils.qrcodes import generate_qr_code_b64, decode_qr_code_b64
from prisma.models import Robots, Paths, Zones , PackageMovement , Packages , ZoneTypes , RobotTypes

from faker import Faker
from faker.providers import BaseProvider

from map_gen.config import (
    MAP ,
    ZONE_TYPE_NAMES ,
    ROWS ,
    COLS ,
    ZONE_TYPE_FOR_ROBOTS ,
    ZONE_TYPE_FOR_ROBOTS_DESC ,
    ZONE_TYPES ,
    ZONE_TYPE_NAMES ,
    ZONE_TYPE_NAMES_DESC ,
    ROBOT_TYPES ,
    ROBOT_NAMES , 
    JETANK ,
    JETRACER ,
    JETANK_HIWONDER ,
    STORAGE
)

from utils.logger import setup_logger
log = setup_logger(__name__)

class RobotProvider(BaseProvider):
    ROBOT_TYPES: list = ROBOT_TYPES

    def robotType(self):
        return self.random_element(self.ROBOT_TYPES)


# FAKE DATA GENERATOR FUNCTIONS =================================================
async def push_fake_packages_to_db(starting_records: int,additional_configuration: dict):
    log.info(f"====== Pushing fake packages ======")
    package_data: list = []
    fake = Faker()

    if starting_records < 0:
        day_to_day_change = 100
    else:
        day_to_day_change = starting_records
     
    # https://www.datacamp.com/tutorial/random-walk
    # https://www.w3schools.com/python/python_datetime.asp
    np_gen = np.random.default_rng(seed=42)
    end_date: datetime = additional_configuration.get("end_date",datetime.now()) 
    insert_date: datetime = additional_configuration.get(
        "start_date",
        datetime(
            year=2024,
            month=1,
            day=1
        )
    )
    packageID = additional_configuration.get("starting_package_ID",1) 
    status_active = False
    try:
        while insert_date <= end_date:
            # fluctuation = int(np_gen.normal(loc=5, scale=15))
            fluctuation = np_gen.choice([-10,-5,0,5,10,15,20])
            day_to_day_change += fluctuation

            if np_gen.random() <= 0.1:
                eventual_drop = np_gen.choice([-100,-50,-30])
            else :
                eventual_drop = 0

            if day_to_day_change < 0:
                day_to_day_change = 0

            if insert_date == end_date:
                status_active = True

            for n in range(day_to_day_change + eventual_drop):
                package_data.append({
                    "packageID"    : packageID,
                    "streetName"   : fake.street_name(),
                    "houseNumber"  : str(random.randint(1,300)),
                    "cityName"     : fake.city(),
                    "cityPostcode" : fake.postcode(),        
                    "insertDate"   : insert_date,
                    "active"       : status_active
                }) 
                packageID += 1
            insert_date += timedelta(days=1)

    except Exception as e:
        log.info(f"Could not create fake packages record for day {insert_date.strftime('%c')} number of records {day_to_day_change} {e}")
        
    try:
        await Packages.prisma().create_many(data=package_data)
    except Exception as e:
        log.info(f"Could not insert fake packages into DB {e}")
        

async def push_fake_zones_to_db(map: list[list[int]],additional_configuration: dict):

    log.info(f"====== Pushing fake zones and zone types ======")
    zone_data_types: list = []
    for zone_type in ZONE_TYPES:
        zone_type_name = ZONE_TYPE_NAMES[zone_type]
        zone_tye_desc = ZONE_TYPE_NAMES_DESC[zone_type] 
        zone_data_types.append({
            "zoneTypeID"   : zone_type,
            "zoneTypeName" : zone_type_name,
            "zoneTypeDescription" : zone_tye_desc,
        })
    try:
        await ZoneTypes.prisma().create_many(data=zone_data_types)
    except Exception as e:
        log.info(f"Could not insert fake zone types into DB {e}")

    zone_data: list = []
    if len(map) > 1:
        if len(map[0]) == 1:
            log.info("defaulting to standard map...")
            map = MAP

    zoneID = 1
    for y in range(ROWS):
        for x in range(COLS):
            zone_type = MAP[y][x]
            zone_type_name = ZONE_TYPE_NAMES[zone_type]

            if zone_type in ZONE_TYPE_FOR_ROBOTS_DESC.keys():
                zone_desc = ZONE_TYPE_FOR_ROBOTS_DESC[zone_type]
            else:
                zone_desc = ""

            zone_name =  zone_type_name + " " +  str(zoneID)

            zone_data.append({
                "zoneID"            : zoneID,              
                "zoneDescription"   : zone_desc,                     
                "zoneName"          : zone_name,                            
                "zoneAvailable"     : True,       
                "zoneType"          : zone_type,            
                "zoneX"             : x,               
                "zoneY"             : y,
                "zoneCapacity"      : 4,               
            })
            zoneID += 1


    try:
        await Zones.prisma().create_many(data=zone_data)
    except Exception as e:
        log.info(f"Could not insert fake zones into DB {e}")
    if additional_configuration.get("add_paths_to_db",False):
        await push_fake_paths_to_db()

async def push_fake_robots_to_db(number_of_records: int,additional_configuration: dict):
    log.info(f"====== Pushing fake robots ======")

    log.info(f"====== Pushing fake zones and zone types ======")
    robot_data_types: list = []
    for robot_type in ROBOT_TYPES:
        robot_type_name = ROBOT_NAMES[robot_type]
        
        robot_data_types.append({
            "robotTypeID"   : robot_type,
            "robotTypeName" : robot_type_name,
        })
    try:
        await RobotTypes.prisma().create_many(data=robot_data_types)
    except Exception as e:
        log.info(f"Could not insert fake robot types into DB {e}")



    robot_data: list = []
    fake = Faker()
    fake.add_provider(RobotProvider)

    if additional_configuration.get("only_jetank",False):
        robot_type_restrication = JETANK
    elif additional_configuration.get("only_jetracer",False):
        robot_type_restrication = JETRACER
    elif additional_configuration.get("only_jetank_hiwonder",False):
        robot_type_restrication = JETANK_HIWONDER
    else:
        robot_type_restrication = "all"


    if number_of_records < 0:
        number_of_records = 40

    robotID = 1
    for x in range(number_of_records):
        if robot_type_restrication == "all":
            robot_type = fake.robotType()
        else:
            robot_type = robot_type_restrication

        robot_ns = ROBOT_NAMES[robot_type] + "_" + str(robotID)

        robot_data.append({
            "robotID"        : robotID,
            "robotStatus"    : True,
            "robotType"      : robot_type,
            "robotNamespace" : robot_ns,
        }) 
        robotID += 1
    try:
        await Robots.prisma().create_many(data=robot_data)
    except Exception as e:
        log.info(f"Could not insert fake robots into DB {e}")

async def push_fake_paths_to_db():
    log.info(f"====== Pushing fake paths ======")
    pass

# NOTE : PM == PackageMovment
async def push_fake_PM_to_db():
    log.info(f"====== Pushing fake PMs ======")
    pass

# NOTE : OM == OrderMovement
async def push_fake_OM_to_db():
    log.info(f"====== Pushing fake OMs ======")
    pass

# FAKE DATA GENERATOR FUNCTIONS =================================================




# main func =================================================
async def push_fake_data_to_db(
    push_packages: bool = True,
    push_zones: bool = True,
    push_robots: bool = True,
    push_paths: bool = True,
    number_of_records: dict = {
        "packages_rec_starting_nbr"  : 100,
        "zones_map"         : MAP,
        "robots_rec_nbr"    : 5,
    }
):
    packages_rec_nbr = number_of_records.get("packages_rec_starting_nbr",100)
    zones_map = number_of_records.get("zones_map",MAP)
    robots_rec_nbr = number_of_records.get("robots_rec_nbr",5)

    push_OM = False
    push_PM = False
    if push_packages and push_zones:
        if push_robots and push_paths:
            push_OM = True
        push_PM = True


    if push_zones:
        await push_fake_zones_to_db(
            map=zones_map,
            additional_configuration={
                "add_paths_to_db" : push_paths
            },
        )
    if push_robots:
        await push_fake_robots_to_db(
            number_of_records=robots_rec_nbr,
            additional_configuration={
                "only_jetank": False,
                "only_jetracer": False,
                "only_jetank_hiwonder": False,
            }
        ) # type: ignore
    if push_packages:
        await push_fake_packages_to_db(
            starting_records=packages_rec_nbr,
            additional_configuration={
                "push_PM": push_PM,
            }
        )

    if push_PM:
        await push_fake_PM_to_db()
        
    if push_OM:
        await push_fake_OM_to_db()
