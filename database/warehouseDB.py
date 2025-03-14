# THIS FILE WILL NOT BE USED IN THE FUTURE !!!

# class Zones(SQLModel, table=True):
#     zoneID: int | None = Field(default=None, primary_key=True)
#     zoneDescription: str = Field(max_length=255)
#     zoneName: str = Field()
#     zoneAvailable: bool = Field(default=True)
#     zoneType: str = Field(default="dropZoneIn")
#     zoneCheck: bool = Field(default=False)

# class Robots(SQLModel, table=True):
#     robotID: int | None = Field(default=None,primary_key=True)
#     robotStatus: bool = Field(default=True) 
#     robotType: str = Field(default="jetank")
#     robotNamespace: str = Field(default=None)

# class Paths(SQLModel, table=True):
#     pathID: int | None = Field(default=None,primary_key=True)
#     pathNumber: int = Field(default=None)
#     pathDescription: str = Field(default="")
#     pathZoneStart: int = Field(default=None,foreign_key="zones.zoneID")
#     pathZoneEnd: int = Field(default=None,foreign_key="zones.zoneID")
#     pathCoordinates: list[int] = Field(sa_column=Column(ARRAY(Integer)))
#     pathActive: bool = Field(default=False)

# class Packages(SQLModel, table=True):
#     packageID: int | None = Field(default=None, primary_key=True)
#     customerID: int | None = Field(default=None)
#     packageCurrentHop: int | None = Field(default=None,foreign_key="zones.zoneID")
#     packageNextHop: int | None = Field(default=None,foreign_key="zones.zoneID") 
#     packageDestinationAddress: str = Field(default="")

# # robot A take Path B to Zone K with Package L
# # think of OrderMovement as a track and trace inside the warehouse
# class OrderMovement(SQLModel,tabele=True):
#     orderMovementID: int | None = Field(default=None,primary_key=True)
#     ZoneID: int | None = Field(default=None,foreign_key="zones.zoneID")
#     RobotID: int | None = Field(default=None,foreign_key="robots.robotID")
#     PathID: int | None = Field(default=None,foreign_key="paths.pathID")
#     PackageID: int | None = Field(default=None,foreign_key="packages.packageID")


