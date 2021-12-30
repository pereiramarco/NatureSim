from aux.Time import Time
from Creature import Creature
from Map import Map

class Game:
    map : Map #map with all the info about the tiles
    creatures = list # list of all creatures on the map

    def __init__(self,width,height,display):
        self.map = Map(width,height,display)
        self.creatures = list()
        
    def creature_in_position(self,position : tuple):
        for creature in self.creatures:
            if creature.position_component.position == position:
                return True
        return False

    def add_creature(self,DISPLAYSURF,pos,sprite_location,food_source,hp,starting_water,water_consumption,starting_food,food_consumption,speed,id):
        creature = Creature(self.map.grid,self.creatures,DISPLAYSURF,pos,sprite_location,food_source,hp,starting_water,water_consumption,starting_food,food_consumption,speed,id)
        self.creatures.append(creature)

    def update(self):
        dead = list()
        for creature in self.creatures:
            died = creature.update()
            if died:
                dead.append(creature)
        for creature in dead:
            self.creatures.remove(creature)
            self.map.add_tile(creature.position_component)
        self.map.update()

    def draw(self):
        self.map.draw()
        for creature in self.creatures:
            creature.draw()
