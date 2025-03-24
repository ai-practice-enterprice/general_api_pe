from pydantic import BaseModel
from typing import Optional


# ===================== Zones Model =====================
class Zones(BaseModel):
    zoneID: int
    zoneDescription: str
    zoneName: str
    zoneAvailable: bool
    zoneType: str
    zoneCheck: bool




# ===================== Robots Model =====================
class Robots(BaseModel):
    robotStatus: bool
    robotType: str
    robotNamespace: Optional[str]




# ===================== Paths Model =====================
class Paths(BaseModel):
    pathID: int
    pathNumber: int
    pathDescription: str
    pathZoneStart: int
    pathZoneEnd: int
    pathCoordinates: str 
    pathActive: bool




# ===================== Packages Model =====================
class Packages(BaseModel):
    packageID: int
    customerID: Optional[int]
    packageCurrentHop: Optional[int]
    packageNextHop: Optional[int]
    packageDestinationAddress: str




# ===================== Order Movement Model =====================
class OrderMovement(BaseModel):
    orderMovementID: int
    ZoneID: int
    RobotID: int
    PathID: int
    PackageID: int
