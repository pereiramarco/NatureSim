from Components.component import Component
import random
import time
from Components.sprite_component import Sprite_Component

from Components.stats_component import Stats_Component
from aux.constants import BUG_FIXING

class Aging_Component(Component):
    born_time : time
    age : int
    stats_component : Stats_Component
    sprite_component : Sprite_Component

    def __init__(self,stats_component, sprite_component):
        self.born_time = time.time()
        self.age = 0
        self.stats_component = stats_component
        self.sprite_component = sprite_component

    def update(self):
        previous_age = self.age
        self.age = int((time.time() - self.born_time)/1) #Ages a year every 10 seconds

        if previous_age<self.age: #Creature aged a year
            if self.age < 10: #Until 10 years old grows in size
                self.stats_component.update_size()
                self.sprite_component.scale_sprite(self.stats_component.size)
            if self.age>50:
                if random.randint(0,2500)<pow(self.age-50,2): #Creature dies of aging
                    self.stats_component.set_hp(0)
        
        if BUG_FIXING:
            self.stats_component.add_stat_to_print("AGE: " + str(self.age))