from Components.position_component import Position_Component
from Components.sprite_component import Sprite_Component 
from aux.auxiliary_functions import get_closest_point
from Temporary_Tile import Temporary_Tile
import aux.constants as constants
from Tile import Tile
import random
import pygame

class Map:
    display : pygame.Surface #display surface

    grid : list #list that holds the entire grid in the form of lists being each line
    tiles : list #list of ground tiles
    temporary_tiles : map #map of position to tile with hitpoints (food)
    width : int # width of the grid
    height : int # height of the grid

    def __init__(self,width,height,display):
        self.width = width
        self.height = height
        self.tiles = list()
        self.temporary_tiles = {}
        self.display = display
        self.create_grid()
        for y in range(self.height):
            for x in range(self.width):
                location = constants.TILESPRITES[self.grid[y][x]]
                position_component = Position_Component((x,y))
                sprite_component = Sprite_Component(display, location, position_component)
                self.tiles.append(Tile(position_component,sprite_component))
                if self.grid[y][x] == 0:
                    if random.randint(1,100) > 99: #puts immovable objects in some places
                        self.add_temporary_tile(position_component,"object",1000)
                    elif random.randint(1,100) > 99: #puts food tile
                        self.add_temporary_tile(position_component,"herbivorous_food",200)

    def add_temporary_tile(self,position_component,tile_name,hitpoints):
        (x,y) = position_component.position
        self.grid[y][x] = constants.TILENAMES[tile_name]
        location =constants.TILESPRITES[self.grid[y][x]]
        sprite_component = Sprite_Component(self.display, location, position_component)
        self.temporary_tiles[position_component.position] = (Temporary_Tile(position_component,sprite_component,hitpoints))
    
    def create_grid(self):
        starting_points = list() # lista de tuplos com os pontos iniciais para a criação aleatória do mapa
        num_of_points = random.randint(20,40)
        for _ in range(num_of_points):
            pos = (random.randint(0,self.width-1),random.randint(0,self.height-1))
            n = random.randint(1,100)
            if n>90:
                point = (pos,1) # water
            else:
                point = (pos,0) # walkable terrain

            if point!= None:
                starting_points.append(point)

        self.grid = list()
        for y in range(self.height):
            self.grid.append(list())
            for x in range(self.width):
                closest_starting_point = get_closest_point((x,y),starting_points)
                self.grid[y].append(closest_starting_point)


    def update(self):
        random_chance = random.randint(1,1000)
        if random_chance > 999:
            while True:
                x = random.randint(0,constants.MAPWIDTH-1)
                y = random.randint(0,constants.MAPHEIGHT-1)
                if self.grid[y][x] == constants.TILENAMES['grass']:
                    position_component = Position_Component((x,y))
                    self.add_temporary_tile(position_component,"herbivorous_food",50)
                    break
        
        finished_tiles = list()
        for tile in self.temporary_tiles.values():
            finished = tile.update()
            if finished == "FINISHED":
                finished_tiles.append(tile.position_component.position)
        for tile in finished_tiles:
            self.temporary_tiles.pop(tile)
            self.grid[tile[1]][tile[0]] = constants.TILENAMES['grass']
        
            

    def draw(self):
        for tile in self.tiles:
            tile.draw()
        for tile in self.temporary_tiles.values():
            tile.draw()