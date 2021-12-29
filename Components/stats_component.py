from Components.position_component import Position_Component
from Components.component import Component
from pygame.font import Font
import aux.constants as constants
import pygame

class Stats_Component(Component):
    id : int
    font : Font
    font_size : int
    display : pygame.Surface
    stats_surfaces : list
    position_component : Position_Component
    hp : int
    water : int
    max_water : int
    speed : float
    temp_speed : float #Speed boost when creature is running

    def __init__(self, display, font_name, font_size, position_component, starting_hp, starting_water, speed, id):
        self.display = display
        self.hp = starting_hp
        self.water = starting_water
        self.max_water = starting_water
        self.speed = speed
        self.temp_speed = 0
        self.font = pygame.font.SysFont(font_name, font_size)
        self.font_size = font_size
        self.position_component = position_component
        self.id = id

    def add_water(self,amount_to_add):
        self.water += amount_to_add

    def add_hp(self,amount_to_add):
        self.hp += amount_to_add
    
    def add_temp_speed(self,amount_to_add):
        self.temp_speed += amount_to_add

    def add_stat(self,stat,amount_to_add):
        eval("self.add_" + stat + "(" + str(amount_to_add) +")")

    def set_water(self,amount_to_set):
        self.water = amount_to_set

    def set_hp(self,amount_to_set):
        self.hp = amount_to_set
    
    def set_temp_speed(self,amount_to_set):
        self.temp_speed = amount_to_set

    def set_stat(self,stat,amount_to_set):
        eval("self.set_" + stat + "(" + str(amount_to_set) +")")
        

    def thirsty(self):
        return self.water/self.max_water < 0.20

    def update(self):
        self.stats_surfaces = list()
        str_to_print = "HP: " + str(self.hp) 
        self.stats_surfaces.append(self.font.render(str_to_print, False, (0,0,0,0)))
        str_to_print = "WTR: " + str(self.water) + "/" + str(self.max_water)
        self.stats_surfaces.append(self.font.render(str_to_print, False, (0,0,0,0)))
        str_to_print = "SPD: " + "{:.1f}".format(self.speed) 
        self.stats_surfaces.append(self.font.render(str_to_print, False, (0,0,0,0)))
        
        if constants.BUG_FIXING:
            str_to_print = "ID: " + str(self.id) 
            self.stats_surfaces.append(self.font.render(str_to_print, False, (0,0,0,0)))
            (x,y) = self.position_component.position
            str_to_print = str((int(x),int(y))) 
            self.stats_surfaces.append(self.font.render(str_to_print, False, (0,0,0,0)))

    def draw(self):
        (position_x,position_y) = self.position_component.position
        for i,surface in enumerate(self.stats_surfaces):
            self.display.blit(surface,(position_x*constants.TILESIZE, (position_y+1)*constants.TILESIZE + i*self.font_size/2))

