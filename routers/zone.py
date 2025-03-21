import logging
import random
from fastapi import APIRouter, Query
from faker import Faker
from faker.config import AVAILABLE_LOCALES
from enum import Enum
from prisma.models import Zones
from typing import Annotated

from config import DB_CLIENT
from database.db_schema import Zones as ZonesSchema


# API endpoints for zone data ==========================================================================
router = APIRouter(prefix="/zones", tags=["Zone Data"])
log = logging.getLogger(__name__)

@router.get("/status",response_model=list[ZonesSchema])
def get_zone_status():
    """
    Get zone data about all zones status and which to check 
    """
    log.info(f"fetching zone data from database")
    
    resultQuery = DB_CLIENT.zones.find_many()

    return  resultQuery

@router.get("/register", response_model=list[ZonesSchema])
def get_register_zone_to_db(
    zone: Annotated[ZonesSchema,Query()] = None,
):
    """
    Add zone to DB
    """
    log.info(f"adding zone to db")
    
    resultQuery = DB_CLIENT.zones.create(zone)

    return resultQuery


@router.post("/generate")
async def generate_random_zones(limit: Annotated[int, Query(ge=1, le=100)] = 1):
    """
    Generate random zones data for testing
    """

    fake = Faker(locale="nl_BE")

    log.info(f"Generating {limit} random zones")
    zones = []

    for _ in range(limit):
        zone_data = {
            "zoneDescription": fake.sentence(nb_words=8),
            "zoneName": fake.word(),
            "zoneAvailable": fake.boolean(chance_of_getting_true=75),
            "zoneType": fake.random_element(elements=("dropZoneIn", "dropZoneOut")),
            "zoneCheck": fake.boolean(chance_of_getting_true=25)
        }


        # Save zone in database
        zone = await Zones.prisma().create(zone_data)
        zones.append(ZonesSchema(**zone.model_dump()))

    log.info(f"Successfully generated and saved {len(zones)} zones")
    return zones