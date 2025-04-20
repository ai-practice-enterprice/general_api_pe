import logging
import os
import random
import httpx
from enum import Enum

from fastapi import APIRouter, Query, HTTPException , Request , Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from prisma.models import Robots, Paths, Zones , PackageMovement , Packages , OrderMovement , ZoneTypes
from typing import Annotated, List
from faker import Faker

from map_gen.MapPlotter import MapPlotter 
from map_gen.config import TILE_SIZE , ZONE_TYPE_FOR_ROBOTS , ZONE_TYPE_FOR_ROBOTS_DESC

from utils.logger import setup_logger
log = setup_logger(__name__)
router = APIRouter(prefix="/frontend", tags=["Frontend"])



# ======================== API endpoints for files ======================== #
# ... maybe