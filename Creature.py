from Components.position_component import Position_Component
from Components.sprite_component import Sprite_Component
from Components.stats_component import Stats_Component
from aux.Time import Time
from aux.auxiliary_functions import distance_between_points
from aux.a_star_pathfinding import astar
import aux.constants as constants
import operator
import random

class Creature: 
    alive : bool #defines if creature is alive or not

    known_grid : list #known part of the map by the creature
    grid : list # complete map

    #Components
    sprite_component : Sprite_Component
    position_component : Position_Component
    stats_component : Stats_Component
    
    current_direction : tuple # describes the creatures current direction
    current_path : list # path that the creature is following (finding water, running, hunting, etc)

    time : Time #class that saves frame passings
    frames_per_step : int #number of frames per step

    def __init__(self,time,grid,display,position,sprite_location,hp,water,speed,id):
        self.current_direction = None
        self.frames_per_step = int(constants.FPS/speed)
        self.time = time
        self.alive = True
        self.grid = grid
        self.known_grid = list()
        self.current_path = None
        for y in range(len(self.grid)):
            self.known_grid.append(list())
            for _ in range(len(self.grid[0])):
                self.known_grid[y].append('?')

        self.position_component = Position_Component(position)
        self.stats_component = Stats_Component(display,"Comic Sans",15,self.position_component,hp,water,speed,id)
        self.sprite_component = Sprite_Component(display,sprite_location,self.position_component)
        self.update_known_grid()

    def update_known_grid(self):
        (position_x,position_y) = self.position_component.position
        for x in range(position_x-1,position_x+2):
            for y in range(position_y-1,position_y+2):
                if 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid):
                    self.known_grid[y][x] = self.grid[y][x]

    #Returns the number of undiscovered tiles on one direction
    def get_undiscovered_number(self,tuple):
        undiscovered = 0
        (x,y) = tuple
        for x_aux in range(x-1,x+2):
            for y_aux in range(y-1,y+2):
                if 0 <= x_aux < len(self.grid[0]) and 0 <= y_aux < len(self.grid):
                    undiscovered += 1 if self.known_grid[y_aux][x_aux]== '?' else 0
        return undiscovered

    #Finds the closest tile of tile_name type to the creature
    def find_closest_tile(self,tile_name):
        tile_number = constants.TILENAMES[tile_name]
        closest = None
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
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
                if 0 <= x_aux < len(self.grid[0]) and 0 <= y_aux < len(self.grid) and self.known_grid[y_aux][x_aux]==tile_type:
                    return True
        return False
    
    #Decides the creature's next move
    def decide_next_direction(self):
        if self.close_to_tile('water') and self.stats_component.thirsty():#creature drinks water
            self.stats_component.add_stat('water',int(self.stats_component.max_water/2))
            self.stats_component.set_stat('temp_speed',0)
            return 'stop'
        if self.current_path != None and len(self.current_path) > 1:
            direction_tuple = tuple(map(operator.sub,self.current_path[0],self.position_component.position[::-1]))
            direction = constants.INVERSE_DIRECTIONS[direction_tuple[::-1]]
            self.current_path = self.current_path[1:]
            return direction
        else:
            self.current_path = None
        if random.randint(1,100)>85 and self.stats_component.temp_speed == 0:#15 percent chance the creature doesn't move unless its running
            return 'stop'
        possible_decisions = set()
        desired_decisions = list()
        #Get all possible directions
        for direction,tuple_dir in constants.DIRECTIONS.items():
            (position_x,position_y) = tuple(map(operator.add, tuple_dir, self.position_component.position))
            if 0 <= position_x < len(self.grid[0]) and 0 <= position_y < len(self.grid) and self.known_grid[position_y][position_x] == 0:
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
        if self.stats_component.hp == 0:
            self.alive = False
        if self.time.frame_counter%constants.FPS==0:
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
                else:
                    self.stats_component.set_stat('temp_speed',1)
            decision = self.decide_next_direction()
            self.current_direction = constants.DIRECTIONS[decision]
            
        self.position_component.update((position_x + self.current_direction[0]/self.frames_per_step,position_y + self.current_direction[1]/self.frames_per_step))
        if self.time.frame_counter%self.frames_per_step==0:
            self.frames_per_step = int(constants.FPS/(self.stats_component.speed + self.stats_component.temp_speed))
            self.position_component.update(tuple(round(itup) for itup in self.position_component.position)) # de forma a remover os erros causados por operações com floats
            self.current_direction=None
        self.stats_component.update()
        
    def draw(self):
        if self.alive:
            self.sprite_component.draw()
            self.stats_component.draw()
