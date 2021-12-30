from Components.position_component import Position_Component
from Components.sprite_component import Sprite_Component 
from aux.auxiliary_functions import get_closest_point
from Tile import Tile
import aux.constants as constants
import random
import pygame

class Map:
    display : pygame.Surface #display surface

    grid : list #list that holds the entire grid in the form of lists being each line
    tiles : list 
    width : int # width of the grid
    height : int # height of the grid

    def __init__(self,width,height,display):
        self.width = width
        self.height = height
        self.tiles = list()
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
                        self.grid[y][x] = constants.TILENAMES["object"]
                        location =constants.TILESPRITES[self.grid[y][x]]
                        sprite_component = Sprite_Component(display, location, position_component)
                        self.tiles.append(Tile(position_component,sprite_component))
                    elif random.randint(1,100) > 99: #puts food tile
                        if random.randint(1,100) > 20:
                            self.grid[y][x] = constants.TILENAMES["herbivorous_food"]
                        else:
                            self.grid[y][x] = constants.TILENAMES["carnivorous_food"]
                        location =constants.TILESPRITES[self.grid[y][x]]
                        sprite_component = Sprite_Component(display, location, position_component)
                        self.tiles.append(Tile(position_component,sprite_component))

    def add_tile(self,position_component):
        (x,y) = position_component.position
        self.grid[y][x] = constants.TILENAMES["carnivorous_food"]
        location =constants.TILESPRITES[self.grid[y][x]]
        sprite_component = Sprite_Component(self.display, location, position_component)
        self.tiles.append(Tile(position_component,sprite_component))
    
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
        if random_chance > 998:
            while True:
                x = random.randint(0,constants.MAPWIDTH-1)
                y = random.randint(0,constants.MAPHEIGHT-1)
                if self.grid[y][x] == constants.TILENAMES['grass']:
                    position_component = Position_Component((x,y))
                    self.grid[y][x] = constants.TILENAMES["herbivorous_food"]
                    location =constants.TILESPRITES[self.grid[y][x]]
                    sprite_component = Sprite_Component(self.display, location, position_component)
                    self.tiles.append(Tile(position_component,sprite_component))
                    break
            

    def draw(self):
        for tile in self.tiles:
            tile.draw()