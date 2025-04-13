import os
from PIL import Image , ImageDraw 

script_path = os.path.dirname(__file__)


# ALL POSSIBLE TILES ===================================================================================
VOID = 0
ROBOT_STATION = 1
STORAGE = 2
ZONE_IN = 3
ERROR_ZONE = 4
NORMAL = 5

ZONE_TYPE_NAMES = {
    VOID : "Void",
    ROBOT_STATION : "RobotStation",
    STORAGE : "Storage",
    ZONE_IN : "DropZoneIn",
    ERROR_ZONE : "ErrorZone",
    NORMAL : "Normal",
}

ZONE_TYPE_FOR_ROBOTS = [
    "RobotStation",
    "Storage",
    "DropZoneIn",
    "ErrorZone",
]

MAP = [
    [ERROR_ZONE, ERROR_ZONE, ERROR_ZONE, ERROR_ZONE, ROBOT_STATION, ROBOT_STATION, ROBOT_STATION, VOID],
    [STORAGE,    STORAGE,    STORAGE,    STORAGE,    VOID,          NORMAL,        NORMAL,        ZONE_IN],
    [STORAGE,    STORAGE,    STORAGE,    STORAGE,    NORMAL,        NORMAL,        NORMAL,        VOID],
    [STORAGE,    STORAGE,    STORAGE,    STORAGE,    VOID,          VOID,          NORMAL,        ZONE_IN],
    [STORAGE,    STORAGE,    STORAGE,    STORAGE,    NORMAL,        NORMAL,        NORMAL,        VOID],
    [STORAGE,    STORAGE,    STORAGE,    STORAGE,    VOID,          VOID,          NORMAL,        ZONE_IN],
]



# colors for the SVG
TILE_COLORS = {
    VOID:           ("#1A1A1A","#959595",0),
    ROBOT_STATION:  ("#1D293B","#5C79A3",0.4),
    STORAGE:        ("#392F3F","#9577A3",0.4),
    ZONE_IN:        ("#1F2F1E","#446E2C",0.4),
    ERROR_ZONE:     ("#512D2B","#D7817E",0.4),
    NORMAL:         ("#36210A","#996500",0.4),
}

# colors for the Image
TILE_TEXTURES = {
    VOID:           Image.open(os.path.join(script_path,"Void.png")).convert("RGBA"),
    ROBOT_STATION:  Image.open(os.path.join(script_path,"Robot_Station.png")).convert("RGBA"),
    STORAGE:        Image.open(os.path.join(script_path,"Storage_Zone.png")).convert("RGBA"),
    ZONE_IN:        Image.open(os.path.join(script_path,"Zone_In.png")).convert("RGBA"),
    ERROR_ZONE:     Image.open(os.path.join(script_path,"Error_Zone.png")).convert("RGBA"),
    NORMAL:         Image.open(os.path.join(script_path,"Normal_Floor.png")).convert("RGBA"),
}

# colors for the lines
LINE_COLOR = (98,252,0,255)
# colors for the dots
DOT_1 = (0,0,255,255)
DOT_2 = (255,0,0,255)

# DRAWING ===================================================================================
TILE_SIZE = 50
WIDTH = len(MAP[0]) * TILE_SIZE
HEIGHT = len(MAP) * TILE_SIZE
ROWS, COLS = len(MAP), len(MAP[0])