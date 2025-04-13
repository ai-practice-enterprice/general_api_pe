import random
import logging
import httpx
from utils.qrcodes import generate_qr_code_b64, decode_qr_code_b64
from prisma.models import Robots, Paths, Zones , PackageMovement , Packages 

from faker import Faker
from faker.providers import BaseProvider

from map_gen.config import MAP , ZONE_TYPE_NAMES , ROWS , COLS , ZONE_TYPE_FOR_ROBOTS

log = logging.getLogger(__name__)

class RobotProvider(BaseProvider):
    ROBOT_TYPES: list = [
        "jetank",
        "jetracer",
        "jetank_hiwonder",
    ]

    def robotType(self):
        return self.random_element(self.ROBOT_TYPES)


# FAKE DATA GENERATOR FUNCTIONS =================================================
async def push_fake_packages_to_db(number_of_records: int,additional_configuration: dict):
    package_data: list[dict] = []
    fake = Faker()

    package_id_range = additional_configuration.get("package_id_range",(1000,1200))
    id_range = package_id_range[1] - package_id_range[0]

    if number_of_records < 0:
        number_of_records = 200

    if id_range < 0 or id_range < number_of_records:
        id_range = number_of_records
     
    for x in range(number_of_records):
        package_data.append({
            "packageID"    : (id_range + x),
            "streetName"   : fake.street_name(),
            "houseNumber"  : str(random.randint(1,300)),
            "cityName"     : fake.city(),
            "cityPostcode" : fake.postcode(),            
        }) 
    try:
        await Packages.prisma().create_many(data=package_data)
    except Exception as e:
        log.info(f"Could not insert fake data into DB {e}")
        

async def push_fake_zones_to_db(map: list[list[int]],additional_configuration: dict,add_paths_to_db: bool = True):
    zone_data: list[dict] = []
    if len(map) > 1:
        if len(map[0]) == 1:
            log.info("defaulting to standard map...")
            map = MAP

    zoneID = 1
    for y in range(ROWS):
        for x in range(COLS):
            zone_type = ZONE_TYPE_NAMES[MAP[y][x]]

            if zone_type in ZONE_TYPE_FOR_ROBOTS:
                zone_data.append({
                    "zoneID"            : zoneID,              
                    "zoneDescription"   : "fake " + zone_type,                     
                    "zoneName"          : zone_type + str(zoneID),                            
                    "zoneAvailable"     : True,       
                    "zoneType"          : zone_type,            
                    "zoneX"             : y,               
                    "zoneY"             : x,               
                })
                zoneID += 1

    try:
        await Zones.prisma().create_many(data=zone_data)
    except Exception as e:
        log.info(f"Could not insert fake data into DB {e}")
    if add_paths_to_db:
        await push_fake_paths_to_db()

async def push_fake_robots_to_db(number_of_records: int,additional_configuration: dict):
    robot_data: list[dict] = []
    fake = Faker()
    fake.add_provider(RobotProvider)

    if additional_configuration.get("only_jetank",False):
        robot_type_restrication = "jetank"
    elif additional_configuration.get("only_jetracer",False):
        robot_type_restrication = "jetracer"
    elif additional_configuration.get("only_jetank_hiwonder",False):
        robot_type_restrication = "jetank_hiwonder"
    else:
        robot_type_restrication = "all"


    if number_of_records < 0:
        number_of_records = 40

    for x in range(number_of_records):
        if robot_type_restrication == "all":
            robot_type = fake.robotType()
        else:
            robot_type = robot_type_restrication

        robot_data.append({
            "robotID"        : (x + 1),
            "robotStatus"    : True,
            "robotType"      : robot_type,
            "robotNamespace" : robot_type + "_" + str(x),
        }) 
    try:
        await Robots.prisma().create_many(data=robot_data)
    except Exception as e:
        log.info(f"Could not insert fake data into DB {e}")

async def push_fake_paths_to_db():
    pass

# NOTE : PM == PackageMovment
async def push_fake_PM_to_db():
    pass

# FAKE DATA GENERATOR FUNCTIONS =================================================




# main func =================================================
async def push_fake_data_to_db(
    push_packages: bool = True,
    push_zones: bool = True,
    push_robots: bool = True,
    push_paths: bool = True,
    number_of_records: dict = {
        "packages_rec_nbr"  : 100,
        "zones_map"         : MAP,
        "robots_rec_nbr"    : 5,
    }
):
    packages_rec_nbr = number_of_records.get("packages_rec_nbr",100)
    zones_map = number_of_records.get("zones_map",MAP)
    robots_rec_nbr = number_of_records.get("robots_rec_nbr",5)

    if push_packages and push_zones:
        push_PM = True
    else:
        push_PM = False

    if push_packages:
        await push_fake_packages_to_db(
            number_of_records=packages_rec_nbr,
            additional_configuration={
                "package_id_range" : (1000,1200)
            }
        )
    if push_zones:
        await push_fake_zones_to_db(
            map=zones_map,
            additional_configuration={},
            add_paths_to_db=push_paths,
        )
    if push_robots:
        await push_fake_robots_to_db(
            number_of_records=robots_rec_nbr,
            additional_configuration={
                "only_jetank": False,
                "only_jetracer": False,
                "only_jetank_hiwonder": False,
            }
        )

    if push_PM:
        await push_fake_PM_to_db()
