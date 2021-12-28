from Components.position_component import Position_Component
from Components.component import Component
from pygame.font import Font
import aux.constants as constants
import pygame

class Stats_Component(Component):
    font : Font
    font_size : int
    display : pygame.Surface
    stats_surfaces : list
    position_component : Position_Component
    hp : int
    water : int
    max_water : int

    def __init__(self, display, font_name, font_size, position_component, starting_hp, starting_water):
        self.display = display
        self.hp = starting_hp
        self.water = starting_water
        self.max_water = starting_water
        self.font = pygame.font.SysFont(font_name, font_size)
        self.font_size = font_size
        self.position_component = position_component

    def add_water(self,amount_to_add):
        self.water += amount_to_add

    def add_hp(self,amount_to_add):
        self.hp += amount_to_add

    def add_stat(self,stat,amount_to_add):
        eval("self.add_" + stat + "(" + str(amount_to_add) +")")

    def thirsty(self):
        return self.water/self.max_water < 0.20

    def update(self):
        self.stats_surfaces = list()
        str_to_print = "HP: " + str(self.hp) 
        self.stats_surfaces.append(self.font.render(str_to_print, False, (0,0,0,0)))
        str_to_print = "WTR: " + str(self.water) + "/" + str(self.max_water)
        self.stats_surfaces.append(self.font.render(str_to_print, False, (0,0,0,0)))

    def draw(self):
        (position_x,position_y) = self.position_component.position
        for i,surface in enumerate(self.stats_surfaces):
            self.display.blit(surface,(position_x*constants.TILESIZE, (position_y+1)*constants.TILESIZE + i*self.font_size/2))

