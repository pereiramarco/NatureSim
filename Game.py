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

    def add_creature(self,creature : Creature):
        self.creatures.append(creature)

    def update(self):
        for creature in self.creatures:
            creature.update()

    def draw(self):
        self.map.draw()
        for creature in self.creatures:
            creature.draw()