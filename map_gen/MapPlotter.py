from PIL import Image , ImageDraw 
import svgwrite
import svgwrite.shapes
from .config import (
    WIDTH , 
    HEIGHT , 
    TILE_COLORS ,
    TILE_TEXTURES,
    TILE_SIZE,
    MAP,
    LINE_COLOR,
    DOT_1,
    DOT_2,
    VOID,
    ZONE_TYPE_NAMES,
    ZONE_TYPE_FOR_ROBOTS
)

class MapPlotter():
    def __init__(
            self,
            size: tuple[int,int] = (WIDTH,HEIGHT),
            tilesize=TILE_SIZE,
            mode="RGBA",
            filename="map",
            ):
        self.filename = filename
        self.WIDTH = size[0]
        self.HEIGHT = size[1]
        self.MAP = MAP
        self.TILE_SIZE = tilesize
        self.TILE_COLORS = TILE_COLORS
        self.TILE_TEXTURES = TILE_TEXTURES
        self.dot_colors = (DOT_1,DOT_2)
        self.clr_lines = LINE_COLOR

        # -------- for the SVG -------- #
        
        
        # -------- for the Image -------- #

        try:
            if mode == "RGBA":
                self.mode =  mode
                # 1) Creating an RGBA image with transparency
                self.image = Image.new(mode="RGBA",size=(self.WIDTH,self.HEIGHT),color=(0,0,0,0))
                self.draw = ImageDraw.Draw(self.image)
            elif mode == "SVG":
                self.mode =  mode
                # 2) Creating an SVG drawing
                # ID's and CLASS names are only added when switching between profiles 
                self.dwg = svgwrite.Drawing(self.filename, size=(self.WIDTH, self.HEIGHT),profile="tiny",class_="warehouse_svg_map")
            else: 
                raise Exception
        except:
            print("Unknown mode")

    def draw_tiles(self):
        # Draw the tiles
        zoneID = 1
        for y, row in enumerate(self.MAP):
            for x, tile in enumerate(row):
                if self.mode == "SVG":
                    zone_type = ZONE_TYPE_NAMES[MAP[y][x]]

                    # -------- for the SVG -------- #
                    color,line_clr, alpha = self.TILE_COLORS[tile]
                    if zone_type in ZONE_TYPE_FOR_ROBOTS:
                        zoneID += 1
                        class_name = "zone"
                        rect = svgwrite.shapes.Rect(
                            insert=(x * self.TILE_SIZE, y * self.TILE_SIZE), 
                            size=(self.TILE_SIZE, self.TILE_SIZE), 
                            fill=color,
                            fill_opacity=alpha,
                            stroke=line_clr,
                            stroke_dasharray="5,5",
                            stroke_width=1,
                            id = str(zoneID),
                            class_ = class_name,
                        )
                    else :
                        class_name = "no_zone"
                        rect = svgwrite.shapes.Rect(
                            insert=(x * self.TILE_SIZE, y * self.TILE_SIZE), 
                            size=(self.TILE_SIZE, self.TILE_SIZE), 
                            fill=color,
                            fill_opacity=alpha,
                            stroke=line_clr,
                            stroke_dasharray="5,5",
                            stroke_width=1,
                            class_ = class_name,
                        )

                    self.dwg.add(rect)

                    

                if self.mode == "RGBA":
                    # -------- for the Image -------- #
                    tile_texture = self.TILE_TEXTURES.get(tile)
                    tile_texture_resized = tile_texture.resize((self.TILE_SIZE, self.TILE_SIZE))
                    self.image.paste(tile_texture_resized, (x * self.TILE_SIZE, y * self.TILE_SIZE), tile_texture_resized)


    def draw_connections(self):
        # Draw connections (horizontal & vertical lines)
        clr_stroke = (self.clr_lines[0],self.clr_lines[1],self.clr_lines[2])
        alpha = self.clr_lines[3]
        for y, row in enumerate(self.MAP):
            for x, tile in enumerate(row):

                if tile == VOID:
                    continue

                center = (x * self.TILE_SIZE + self.TILE_SIZE // 2, y * self.TILE_SIZE + self.TILE_SIZE // 2)
                # -------- Horizontal Lines -------- ""
                if x < len(row) - 1 and MAP[y][x + 1] != VOID:
                    if self.mode == "SVG":

                        # -------- for the SVG -------- #
                        self.dwg.add(
                            svgwrite.shapes.Line(
                                start=(x * self.TILE_SIZE + self.TILE_SIZE // 2, y * self.TILE_SIZE + self.TILE_SIZE // 2),
                                end=((x + 1) * self.TILE_SIZE + self.TILE_SIZE // 2, y * self.TILE_SIZE + self.TILE_SIZE // 2),
                                stroke="rgb" + str(clr_stroke),
                                stroke_opacity=0.8,
                                stroke_width=4,
                            )
                        )

                    if self.mode == "RGBA":
                        # -------- for the Image -------- #
                        self.draw.line(
                            [center, (x * self.TILE_SIZE + self.TILE_SIZE + self.TILE_SIZE // 2, y * self.TILE_SIZE + self.TILE_SIZE // 2)],
                            fill=self.clr_lines,
                            width=4
                        )

                # -------- Vertical Lines -------- #
                if y < len(self.MAP) - 1 and self.MAP[y + 1][x] != VOID:
                    if self.mode == "SVG":
                        # -------- for the SVG -------- #
                        self.dwg.add(
                            svgwrite.shapes.Line(
                                start=(x * self.TILE_SIZE + self.TILE_SIZE // 2, y * self.TILE_SIZE + self.TILE_SIZE // 2),
                                end=(x * self.TILE_SIZE + self.TILE_SIZE // 2, (y + 1) * self.TILE_SIZE + self.TILE_SIZE // 2),
                                stroke="rgb" + str(clr_stroke),
                                stroke_width=4,
                                stroke_opacity=0.8,
                            )
                        )

                    if self.mode == "RGBA":
                        # -------- for the Image -------- #
                        self.draw.line(
                            [center, (x * self.TILE_SIZE + self.TILE_SIZE // 2, y * self.TILE_SIZE + self.TILE_SIZE + self.TILE_SIZE // 2)],
                            fill=self.clr_lines,
                            width=4
                        )

    def draw_centers(self,radius=5):
        
        for y, row in enumerate(self.MAP):
            for x, tile in enumerate(row):
                if tile == VOID:
                    continue

                if (x + y) % 2 : 
                    clr = self.dot_colors[0]
                else:
                    clr = self.dot_colors[1]
     
                center = (x * self.TILE_SIZE + self.TILE_SIZE // 2, y * self.TILE_SIZE + self.TILE_SIZE // 2)
                if self.mode == "SVG":
                    # -------- for the SVG -------- #
                    self.dwg.add(
                        svgwrite.shapes.Circle(
                            center=center,
                            r=radius,
                            stroke="rgb" + str((clr[0],clr[1],clr[2])),
                            stroke_width=2,
                            fill="rgb" + str((clr[0],clr[1],clr[2])),
                            fill_opacity=0.3
                        )
                    )

                if self.mode == "RGBA":
                    # -------- for the Image -------- #
                    self.draw.ellipse(
                        [(center[0] - radius, center[1] - radius),(center[0] + radius, center[1] + radius)],
                        fill=clr,
                        width=4
                    )
               

    def save_map(self):
        if self.mode == "SVG":
            # -------- for the SVG -------- #
            self.dwg.save()
        if self.mode == "RGBA":
            # -------- for the Image -------- #
            self.image.save(self.filename)

