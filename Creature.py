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
    id : int #Identifier of creature
    alive : bool #defines if creature is alive or not

    known_grid : list #known part of the map by the creature
    temporary_tiles : map #Map of position to temporary tiles in the grid
    grid : list # complete map
    creatures : list #List of creatures

    #Components
    sprite_component : Sprite_Component
    position_component : Position_Component
    stats_component : Stats_Component
    follow_component : Follow_Component
    
    current_direction : tuple # describes the creatures current direction
    current_path : list # path that the creature is following (finding water, running, hunting, etc)

    def __init__(self,grid,temporary_tiles,creatures,display,position,sprite_location,
                food_source,hp,
                water,water_consumption,
                food,food_consumption,
                speed,vision,id,species,
                sex):
        self.alive = True
        self.id = id
        self.grid = grid
        self.temporary_tiles = temporary_tiles
        self.known_grid = list()
        self.creatures = creatures
        self.current_path = None
        self.current_direction = None
        for y in range(len(self.grid)):
            self.known_grid.append(list())
            for _ in range(len(self.grid[0])):
                self.known_grid[y].append('?')

        self.position_component = Position_Component(position)
        self.stats_component = Stats_Component(display,"Comic Sans",constants.FONTSIZE,self.position_component,food_source,hp,water,water_consumption,food,food_consumption,speed,vision,id,species,sex)
        self.sprite_component = Sprite_Component(display,sprite_location,self.position_component)
        self.follow_component = None

    def update_known_grid(self):
        (position_x,position_y) = tuple( round(tup) for tup in self.position_component.position)
        vision = self.stats_component.vision
        for x in range(position_x-vision,position_x+vision+1):
            for y in range(position_y-vision,position_y+vision+1):
                if 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid):
                    self.known_grid[y][x] = self.grid[y][x]

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
                        return (x_aux,y_aux)
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
                if closest_needed_tile == None and self.stats_component.food_source in ['carnivorous','omnivorous']:
                    closest_id,closest_creature = self.get_closest_creature_in_radius(self.stats_component.vision)
                    if closest_id != None: #Has any creature close to him
                        self.follow_component = Follow_Component(self.known_grid,self.id,self.position_component,closest_id,closest_creature)
                self.stats_component.set_stat('temp_speed',1)
            if closest_needed_tile != None:
                path = astar(self.known_grid, self.position_component.position ,closest_needed_tile)
                self.current_path = None if path==None else path[1:]
        
        if self.current_path != None and len(self.current_path)>1:
            direction_tuple = tuple(map(operator.sub,self.current_path[0][::-1],self.position_component.position))
            direction = constants.INVERSE_DIRECTIONS[direction_tuple]
            self.current_path = self.current_path[1:]
            return direction

    #Is position known
    def  is_position_known(self,position):
        (x,y) = position
        return self.grid[round(y)][round(x)] == constants.TILENAMES['grass']

    #Decides the closest creature
    def get_closest_creature_in_radius(self,radius):
        closest = None
        closest_id = None
        closest_distance = None
        for creature in self.creatures.values():
            if creature.id == self.id or (creature.stats_component.species == self.stats_component.species and not self.stats_component.starving()):
                continue
            else:
                creature_distance = distance_between_points(self.position_component.position,creature.position_component.position)
                if closest == None or closest_distance > creature_distance and creature_distance <= radius and self.is_position_known(creature.position_component.position):
                    closest = creature.position_component
                    closest_id = creature.id
                    closest_distance = creature_distance
        return closest_id,closest

    def get_possible_decisions(self):
        possible_decisions = set()
        for direction,tuple_dir in constants.DIRECTIONS.items():
            (position_x,position_y) = tuple(map(operator.add, tuple_dir, self.position_component.position))
            if 0 <= position_x < len(self.grid[0]) and 0 <= position_y < len(self.grid) and self.known_grid[position_y][position_x] == 0:
                possible_decisions.add(direction)
        return possible_decisions
        
    #If creature is hungry or thirsty 
    def interaction(self):
        
        if self.stats_component.thirsty():#creature drinks water
            position = self.close_to_tiles(['water'])
            if position:
                self.stats_component.add_stat('water',int(self.stats_component.max_water/2))
                self.stats_component.set_stat('temp_speed',0) #Sets the temporary speed of the creature to 0 because the alarm of thirst has stopped
                self.current_path = None
                return 'stop'
        
        if self.stats_component.hungry():#creature feeds itself
            position = self.close_to_tiles(constants.FOOD_TYPES[self.stats_component.food_source])
            if position:
                tile = self.temporary_tiles[position]
                max_food_to_eat = int(min(self.stats_component.max_food-self.stats_component.food,tile.hitpoints))
                amount_food_eaten = random.randint(int(max_food_to_eat/2),max_food_to_eat)
                self.stats_component.add_stat('food',amount_food_eaten)
                tile.hitpoints-=amount_food_eaten
                self.stats_component.set_stat('temp_speed',0) #Sets the temporary speed of the creature to 0 because the alarm of hunger has stopped
                self.current_path = None
                return 'stop'

    #Decides the creature's next move
    def decide_next_direction(self):

        #Decides if creature will eat or drink
        decision = self.interaction()
        if decision:
            return decision
        
        #Continues previous decided path or calculates a new one if needed
        direction = self.decide_path()
        if direction!= None:
            return direction

        if self.follow_component != None: #If following a creature continues to follow 
            return self.follow_component.update(self.get_possible_decisions())
        
        #Wanders through the map if not on a mission to go somewhere
        if random.randint(1,100)>85 and self.current_path == None:#15 percent chance the creature doesn't move unless its on a mission
            return 'stop'
        
        #Else chooses a direction from all possible
        possible_decisions = list(self.get_possible_decisions())
        decision = possible_decisions[random.randint(0,len(possible_decisions)-1)]
        return decision
    
    #Takes care of the interactions that happened with this animal
    def treat_interactions(self, interactions):
        if interactions:
            stat_interactions = list()
            for interaction in interactions:
                (interaction_type,id) = interaction
                if interaction_type == "StopFollow":
                    self.follow_component = None
                    self.update_known_grid() #If stopped followinf updates grid in case he killed
                else:
                    stat_interactions.append(interaction)
            return stat_interactions


    def update(self,interactions):

        frames_per_step = self.stats_component.frames_per_step

        #Update the creature stats
        stat_interactions = self.treat_interactions(interactions)
        self.alive,finished_step = self.stats_component.update(stat_interactions)
        if self.alive == False:
            return ("Death",self.id,None)
        
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

        if self.follow_component != None and self.follow_component.distance() < 1:
            return ("Attack",self.follow_component.id_follower,self.follow_component.id_followed)
        
    def draw(self):
        if self.alive:
            self.sprite_component.draw()
            self.stats_component.draw()
