from aux.Time import Time
from Creature import Creature
from Map import Map

class Game:
    map : Map #map with all the info about the tiles
    creatures : map # map of all creatures on the map
    interactions : map #map of all interactions between creatures from one frame to the next

    def __init__(self,width,height,display):
        self.map = Map(width,height,display)
        self.creatures = {}
        self.interactions = {}
        
    def creature_in_position(self,position : tuple):
        for creature in self.creatures.values():
            if creature.position_component.position == position:
                return True
        return False

    def add_creature(self,DISPLAYSURF,pos,sprite_location,food_source,hp,starting_water,water_consumption,starting_food,food_consumption,speed,vision,id,species):
        creature = Creature(self.map.grid,self.map.temporary_tiles,self.creatures,DISPLAYSURF,pos,sprite_location,food_source,hp,starting_water,water_consumption,starting_food,food_consumption,speed,vision,id,species)
        self.creatures[id] = creature

    def update(self):
        dead = list()

        for creature in self.creatures.values():
            interactions = self.interactions.get(creature.id)
            info = creature.update(interactions)
            self.interactions[creature.id] = list()
            if info != None:
                (interaction_type,id_1,id_2) = info
                if interaction_type == "Death":
                    dead.append((creature,id_1))
                if interaction_type == "Attack":
                    self.interactions[id_2].append(("Attack",id_1))
        for (creature,id) in dead:
            self.creatures.pop(id)
            self.map.add_temporary_tile(creature.position_component,"carnivorous_food",50)
            for creature in self.creatures.values(): #Tell creatures that followed this animal to stop following
                if creature.follow_component != None and creature.follow_component.id_followed == id:
                    self.interactions[creature.id].append(("StopFollow",id))
        self.map.update()

    def draw(self):
        self.map.draw()
        for creature in self.creatures.values():
            creature.draw()
