import logging
import random
from fastapi import APIRouter, Query
from faker import Faker
from faker.config import AVAILABLE_LOCALES
from enum import Enum
from typing import Annotated

from config import DB_CLIENT
from database.db_schema import *


# API endpoints for zone data ==========================================================================
router = APIRouter(prefix="/zones", tags=["Zone Data"])
log = logging.getLogger(__name__)

@router.get("/status",response_model=list[Zones])
def get_zone_status():
    """
    Get zone data about all zones status and which to check 
    """
    log.info(f"fetching zone data from database")
    
    resultQuery = DB_CLIENT.zones.find_many()

    return  resultQuery

@router.get("/register", response_model=list[Zones])
def get_register_zone_to_db(
    zone: Annotated[Zones,Query()] = None,
):
    """
    Add zone to DB
    """
    log.info(f"adding zone to db")
    
    resultQuery = DB_CLIENT.zones.create(zone)

    return resultQuery