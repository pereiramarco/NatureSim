from Components.follow_component import Follow_Component
from Components.position_component import Position_Component
from Components.sprite_component import Sprite_Component
from Components.stats_component import Stats_Component
from aux.auxiliary_functions import distance_between_points
from aux.a_star_pathfinding import astar
import aux.constants as constants
import operator
import random

class Creature: 
    alive : bool #defines if creature is alive or not

    known_grid : list #known part of the map by the creature
    grid : list # complete map
    creatures : list #List of creatures

    #Components
    sprite_component : Sprite_Component
    position_component : Position_Component
    stats_component : Stats_Component
    follow_component : Follow_Component
    
    current_direction : tuple # describes the creatures current direction
    current_path : list # path that the creature is following (finding water, running, hunting, etc)

    def __init__(self,grid,creatures,display,position,sprite_location,
                food_source,hp,
                water,water_consumption,
                food,food_consumption,
                speed,id):
        self.alive = True
        self.grid = grid
        self.known_grid = list()
        self.creatures = creatures
        self.current_path = None
        self.current_direction = None
        for y in range(len(self.grid)):
            self.known_grid.append(list())
            for _ in range(len(self.grid[0])):
                self.known_grid[y].append('?')

        self.position_component = Position_Component(position)
        self.stats_component = Stats_Component(display,"Comic Sans",constants.FONTSIZE,self.position_component,food_source,hp,water,water_consumption,food,food_consumption,speed,id)
        self.sprite_component = Sprite_Component(display,sprite_location,self.position_component)
        self.follow_component = None
        #if (id != 0):
        #    self.follow_component = Follow_Component(self.grid,self.position_component,self.get_closest_creature())

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

    #Finds the closest tile in tile_names to the creature
    def find_closest_tiles(self,tile_names):
        closest = None
        for tile_name in tile_names:
            tile_number = constants.TILENAMES[tile_name]
            for y in range(len(self.grid)):
                for x in range(len(self.grid[0])):
                    if self.known_grid[y][x]==tile_number:
                        dist = distance_between_points(self.position_component.position,(x,y))
                        if closest == None or dist < distance_between_points(self.position_component.position,closest):
                            closest = (x,y)
        return closest
    
    #Returns True if the creature is close to tiles of type in tile_names
    def close_to_tiles(self,tile_names):
        for tile_name in tile_names:
            tile_type = constants.TILENAMES[tile_name]
            positions_to_check = [(1,0),(-1,0),(0,1),(0,-1)]
            for pos in positions_to_check:
                    (x_aux,y_aux) = tuple(map(operator.add,pos,self.position_component.position))
                    if 0 <= x_aux < len(self.grid[0]) and 0 <= y_aux < len(self.grid) and self.known_grid[y_aux][x_aux]==tile_type:
                        return True
        return False
    
    #Decides path to be followed or continues previously decided path
    def decide_path(self):
        if self.current_path == None:
            closest_needed_tile = None
            if self.stats_component.thirsty():# if it's thirtsty and knows where water is follows path to it
                closest_needed_tile = self.find_closest_tiles(['water'])
                self.stats_component.set_stat('temp_speed',1)
            elif self.stats_component.hungry():# if it's hungry and knows where food is follows path to it
                closest_needed_tile = self.find_closest_tiles(constants.FOOD_TYPES[self.stats_component.food_source])
                self.stats_component.set_stat('temp_speed',1)
            if closest_needed_tile != None:
                path = astar(self.known_grid, self.position_component.position ,closest_needed_tile)
                self.current_path = None if path==None else path[1:]
        
        if self.current_path != None and len(self.current_path)>1:
            direction_tuple = tuple(map(operator.sub,self.current_path[0][::-1],self.position_component.position))
            direction = constants.INVERSE_DIRECTIONS[direction_tuple]
            self.current_path = self.current_path[1:]
            return direction
    
    #Decides the closest creature
    def get_closest_creature(self):
        closest = self.creatures[0].position_component
        for creature in self.creatures[1:]:
            if creature.stats_component.id == self.stats_component.id:
                continue
            else:
                if distance_between_points(self.position_component.position,closest.position) > distance_between_points(self.position_component.position,creature.position_component.position):
                    closest = creature.position_component
        return closest

    def get_possible_decisions(self):
        possible_decisions = set()
        for direction,tuple_dir in constants.DIRECTIONS.items():
            (position_x,position_y) = tuple(map(operator.add, tuple_dir, self.position_component.position))
            if 0 <= position_x < len(self.grid[0]) and 0 <= position_y < len(self.grid) and self.known_grid[position_y][position_x] == 0:
                possible_decisions.add(direction)
        return possible_decisions
        
    #Decides the creature's next move
    def decide_next_direction(self):

        if self.follow_component != None: #If following a creature continues to follow 
            return self.follow_component.update(self.get_possible_decisions())

        if self.close_to_tiles(['water']) and self.stats_component.thirsty():#creature drinks water
            self.stats_component.add_stat('water',int(self.stats_component.max_water/2))
            self.stats_component.set_stat('temp_speed',0) #Sets the temporary speed of the creature to 0 because the alarm of thirst has stopped
            self.current_path = None
            return 'stop'
        
        if self.close_to_tiles(constants.FOOD_TYPES[self.stats_component.food_source]) and self.stats_component.hungry():#creature feeds itself
            self.stats_component.add_stat('food',int(self.stats_component.max_food/2))
            self.stats_component.set_stat('temp_speed',0) #Sets the temporary speed of the creature to 0 because the alarm of hunger has stopped
            self.current_path = None
            return 'stop'
        
        #Continues previous decided path or calculates a new one if needed
        direction = self.decide_path()
        if direction!= None:
            return direction
        
        #Wanders through the map if not on a mission to go somewhere
        if random.randint(1,100)>85 and self.current_path == None:#15 percent chance the creature doesn't move unless its on a mission
            return 'stop'
        possible_decisions = set()
        desired_decisions = list()
        #Get all possible directions
        possible_decisions = self.get_possible_decisions()
        
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

        frames_per_step = self.stats_component.frames_per_step

        #Update the creature stats
        self.alive,finished_step = self.stats_component.update()
        if self.alive == False:
            return "DIED"
        
        #Decides next_direction
        (position_x,position_y) = self.position_component.position
        if self.current_direction == None:
            self.update_known_grid()
            decision = self.decide_next_direction()
            self.current_direction = constants.DIRECTIONS[decision]
        

        #Update position  
        self.position_component.update((position_x + self.current_direction[0]/frames_per_step,position_y + self.current_direction[1]/frames_per_step))
        if finished_step:
            self.position_component.update(tuple(round(itup) for itup in self.position_component.position)) # de forma a remover os erros causados por operações com floats
            self.current_direction=None
        
    def draw(self):
        if self.alive:
            self.sprite_component.draw()
            self.stats_component.draw()
