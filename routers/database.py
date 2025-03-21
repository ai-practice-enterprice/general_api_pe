import logging
from fastapi import APIRouter
from config import DB_CLIENT
from database.db_schema import *

router = APIRouter(prefix="/database", tags=["Database"])
log = logging.getLogger(__name__)

@router.get("/live", response_model=dict)
async def get_database_content():
    """
    Get all data from all database tables
    """
    log.info("Fetching all database content")

    try:
        zones = await DB_CLIENT.zones.find_many()
        robots = await DB_CLIENT.robots.find_many()
        paths = await DB_CLIENT.paths.find_many()
        packages = await DB_CLIENT.packages.find_many()
        order_movements = await DB_CLIENT.order_movement.find_many()

        return {
            "Zones": zones,
            "Robots": robots,
            "Paths": paths,
            "Packages": packages,
            "OrderMovements": order_movements
        }

    except Exception as e:
        log.error(f"Error collecting data: {e}")
        return {"error": str(e)}
