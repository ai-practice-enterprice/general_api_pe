import logging
import random
from fastapi import APIRouter, Query
from config import DB_CLIENT



# API endpoints for workers ==========================================================================
router = APIRouter(prefix="/workers", tags=["Worker Data"])
log = logging.getLogger(__name__)

@router.get("/arrival", response_model=str)
def worker_arrival_confirmation(
    _worker_id: int,
    _zone_id: int,
):
    """
    Confirms that the driver has arrived at the warehouse and assigns an available load-out zone.
    In this example, load-out zones in the database are marked with 'zoneType' equal to "loadOut"
    and are considered available if 'zoneAvailable' is True.
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

