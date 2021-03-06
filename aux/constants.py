BUG_FIXING = True
TILESIZE = 32
MAPHEIGHT = 30
MAPWIDTH = 60
FPS = 30
TIMEPERFRAME = 0.3/FPS
FONTSIZE = 18
TILESPRITES = {
    0 : "assets/tiles/free_tile.png",
    1 : "assets/tiles/water_tile.png",
    2 : "assets/tiles/food_herbivorous_tile.png",
    3 : "assets/tiles/food_carnivorous_tile.png",
    4 : "assets/tiles/imovable_tile.png"
}
TILENAMES = {
    'grass' : 0,
    'water' : 1,
    'herbivorous_food' : 2,
    'carnivorous_food' : 3,
    'object' : 4
}
DIRECTIONS = {
    "up": (0,-1),
    "down":(0,1),
    "right":(1,0),
    "left":(-1,0),
    "upright":(1,-1),
    "upleft":(-1,-1),
    "downright":(1,1),
    "downleft":(-1,1),
    "stop":(0,0),
}
INVERSE_DIRECTIONS = {
    (0,-1):"up",
    (0,1):"down",
    (1,0):"right",
    (-1,0):"left",
    (1,-1):"upright",
    (-1,-1):"upleft",
    (1,1):"downright",
    (-1,1):"downleft",
    (0,0):"stop"
}
FOOD_TYPES = {
    "herbivorous" : ['herbivorous_food'],
    "omnivorous" : ['herbivorous_food','carnivorous_food'],
    "carnivorous" : ['carnivorous_food']
}