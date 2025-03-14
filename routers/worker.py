import logging
import random
from fastapi import APIRouter, Query
from config import DB_CLIENT



# API endpoints for workers ==========================================================================
router = APIRouter(prefix="/workers", tags=["Worker Data"])
log = logging.getLogger(__name__)

@router.get("/arrival",response_model=str)
def get_worker_arrival_confirmation(
    _worker_id: int,
    _zone_id: int,
):
    """
    Get a Okay response from the server, when arriving
    """
    log.info(f"sending response to worker (arriving at warehouse)")

    return str(f"Okay Worker arrived at zone {_zone_id}")
    

@router.get("/departure",response_model=str)
def get_worker_departure_confirmation(
    _worker_id: int,
    _zone_id: int,
):
    """
    Get a Okay response from the server, when departing
    """
    log.info(f"sending response to worker (leaving from warehouse)")

    return str(f"Okay Worker departed from zone {_zone_id}")

