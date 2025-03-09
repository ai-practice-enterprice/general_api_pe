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
def add_zone_info(index: int,zone: zone):
    if index < 0 or index > len(zones):
        raise HTTPException(status_code=400, detail="Index out of range")
    if index < len(zones):
        zones.pop(index)
    zones.insert(index, zone)
    return zone