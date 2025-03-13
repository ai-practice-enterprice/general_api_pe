from pydantic import BaseModel

import logging
from fastapi import APIRouter, HTTPException
from typing import  List


router = APIRouter(prefix="/camera", tags=["zone Data"])
log = logging.getLogger(__name__)


class zone(BaseModel):
    id: int
    status: bool
    detection: bool


zones: List[zone] = []


@router.get("/zoneinfo", response_model=List[zone])
def get_zone_info():
    return zones



@router.post("/zoneinfo", response_model=zone)
def add_zone_info(zone: zone):
    index=zone.id
    for i, x in enumerate(zones):
        if x.id == zone.id:
            zones[i] = zone
            break
    else:
        zones.append(zone)
    return zone