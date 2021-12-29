from Components.position_component import Position_Component
from Components.sprite_component import Sprite_Component
from Components.stats_component import Stats_Component
from aux.auxiliary_functions import distance_between_points
from aux.a_star_pathfinding import astar
import aux.constants as constants
import operator
import random

class Creature: 
    known_grid : list #known part of the map by the creature
    grid : list # complete map
    width_of_grid : int # width of map
    height_of_grid : int # height of map
    sprite_component : Sprite_Component
    position_component : Position_Component
    stats_component : Stats_Component
    alive : bool #defines if creature is alive or not
    current_direction : tuple # describes the creatures current direction
    next_position : tuple #saves the position where the creature is heading
    frame : int # frame number 
    current_path : list # path that the creature is following (finding water, running, hunting, etc)

    def __init__(self,grid,width_of_grid,height_of_grid,display,position,sprite_location,hp,water,id):
        self.current_direction = None
        self.frame = 0
        self.alive = True
        self.grid = grid
        self.width_of_grid = width_of_grid
        self.height_of_grid = height_of_grid
        self.known_grid = list()
        self.current_path = None
        for y in range(self.height_of_grid):
            self.known_grid.append(list())
            for _ in range(self.width_of_grid):
                self.known_grid[y].append('?')

        self.position_component = Position_Component(position)
        self.stats_component = Stats_Component(display,"Comic Sans",15,self.position_component,hp,water,id)
        self.sprite_component = Sprite_Component(display,sprite_location,self.position_component)
        self.update_known_grid()

    def update_known_grid(self):
        (position_x,position_y) = self.position_component.position
        for x in range(position_x-1,position_x+2):
            for y in range(position_y-1,position_y+2):
                if 0 <= x < self.width_of_grid and 0 <= y < self.height_of_grid:
                    self.known_grid[y][x] = self.grid[y][x]

    #Returns the number of undiscovered tiles on one direction
    def get_undiscovered_number(self,tuple):
        undiscovered = 0
        (x,y) = tuple
        for x_aux in range(x-1,x+2):
            for y_aux in range(y-1,y+2):
                if 0 <= x_aux < self.width_of_grid and 0 <= y_aux < self.height_of_grid:
                    undiscovered += 1 if self.known_grid[y_aux][x_aux]== '?' else 0
        return undiscovered

    #Finds the closest tile of tile_name type to the creature
    def find_closest_tile(self,tile_name):
        tile_number = constants.TILENAMES[tile_name]
        closest = None
        for y in range(self.height_of_grid):
            for x in range(self.width_of_grid):
                if self.known_grid[y][x]==tile_number:
                    dist = distance_between_points(self.position_component.position,(x,y))
                    if closest == None or dist < distance_between_points(self.position_component.position,closest):
                        closest = (x,y)
        return closest
    
    #Returns True if the creature is close to tile of type tile_name
    def close_to_tile(self,tile_name):
        tile_type = constants.TILENAMES[tile_name]
        positions_to_check = [(1,0),(-1,0),(0,1),(0,-1)]
        for pos in positions_to_check:
                (x_aux,y_aux) = tuple(map(operator.add,pos,self.position_component.position))
                if 0 <= x_aux < self.width_of_grid and 0 <= y_aux < self.height_of_grid and self.known_grid[y_aux][x_aux]==tile_type:
                    return True
        return False
    
    #Decides the creature's next move
    def decide_next_direction(self):
        if self.close_to_tile('water') and self.stats_component.thirsty():#creature drinks water
            self.stats_component.add_stat('water',int(self.stats_component.max_water/2))
            return 'stop'
        if self.current_path != None and len(self.current_path) > 1:
            direction_tuple = tuple(map(operator.sub,self.current_path[0],self.position_component.position[::-1]))
            direction = constants.INVERSE_DIRECTIONS[direction_tuple[::-1]]
            self.current_path = self.current_path[1:]
            return direction
        else:
            self.current_path = None
        if random.randint(1,100)>85:#15 percent chance the creature doesn't move
            return 'stop'
        possible_decisions = set()
        desired_decisions = list()
        #Get all possible directions
        for direction,tuple_dir in constants.DIRECTIONS.items():
            (position_x,position_y) = tuple(map(operator.add, tuple_dir, self.position_component.position))
            if 0 <= position_x < self.width_of_grid and 0 <= position_y < self.height_of_grid and self.known_grid[position_y][position_x] == 0:
                possible_decisions.add(direction)
        
        #Get only directions that discover part of the map
        for direction, tuple_dir in constants.DIRECTIONS.items():
            if direction in possible_decisions:
                position_to_check = tuple(map(operator.add, tuple_dir, self.position_component.position))
                undiscovered = self.get_undiscovered_number(position_to_check)
                desired_decisions.extend([direction for _ in range(undiscovered)])
        
        if len(desired_decisions) == 0:
            desired_decisions = list(possible_decisions)
        decision = desired_decisions[random.randint(0,len(desired_decisions)-1)]
        return decision

    def update(self):
        if self.alive == False:
            return
        self.frame+=1
        if self.stats_component.hp == 0:
            self.alive = False
        if self.frame==constants.FPS:
            if self.stats_component.water == 0:
                self.stats_component.add_stat("hp",-1)
            else:
                self.stats_component.add_stat("water",-1)
        (position_x,position_y) = self.position_component.position
        if self.current_direction == None:
            self.update_known_grid()
            if self.stats_component.thirsty():# if it's thirtsty and knows where water is follows path to it
                closest_water_tile = self.find_closest_tile('water')
                if closest_water_tile != None:
                    self.current_path = astar(self.known_grid, self.position_component.position ,closest_water_tile)
                    self.current_path = None if self.current_path==None else self.current_path[1:]
            decision = self.decide_next_direction()
            self.current_direction = constants.DIRECTIONS[decision]
            self.next_position = tuple(map(operator.add, self.current_direction, self.position_component.position))
            
        self.position_component.update((position_x + self.current_direction[0]/constants.FPS,position_y + self.current_direction[1]/constants.FPS))
        if self.frame==constants.FPS:
            self.frame=0
            self.position_component.update(self.next_position) # de forma a remover os erros causados por operações com floats
            self.current_direction=None
        self.stats_component.update()
        
    def draw(self):
        if self.alive:
            self.sprite_component.draw()
            self.stats_component.draw()
