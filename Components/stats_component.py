from pygame.display import update
from Components.position_component import Position_Component
from Components.component import Component
from pygame.font import Font
from aux.Time import Time
from aux.a_star_pathfinding import return_path
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
    water_consumption_per_step : float
    water : float
    max_water : int
    food_source : str
    food_consumption_per_step : float
    food : float
    max_food : int
    speed : float
    temp_speed : float #Speed boost when creature is running
    frames_per_step : float #Number of frames per step
    time : Time #Class responsible for controlling frame passage

    def __init__(self, display, font_name, font_size, position_component, food_source, starting_hp, starting_water, water_consumption, starting_food, food_consumption, speed, id):
        self.display = display
        self.hp = starting_hp
        self.food_source = food_source
        self.water = starting_water
        self.max_water = starting_water
        self.water_consumption_per_step = water_consumption
        self.food = starting_food
        self.max_food = starting_food
        self.food_consumption_per_step = food_consumption
        self.speed = speed
        self.temp_speed = 0
        self.font = pygame.font.SysFont(font_name, font_size)
        self.font_size = font_size
        self.position_component = position_component
        self.id = id
        self.time = Time()
        self.frames_per_step = int(constants.FPS/(self.speed))
        self.stats_surfaces = list()

    def add_water(self,amount_to_add):
        self.water += amount_to_add

    def add_food(self,amount_to_add):
        self.food += amount_to_add

    def add_hp(self,amount_to_add):
        self.hp += amount_to_add
    
    def add_temp_speed(self,amount_to_add):
        self.temp_speed += amount_to_add

    def add_stat(self,stat,amount_to_add):
        eval("self.add_" + stat + "(" + str(amount_to_add) +")")

    def set_water(self,amount_to_set):
        self.water = amount_to_set
    
    def set_food(self,amount_to_set):
        self.food = amount_to_set

    def set_hp(self,amount_to_set):
        self.hp = amount_to_set
    
    def set_temp_speed(self,amount_to_set):
        self.temp_speed = amount_to_set

    def set_stat(self,stat,amount_to_set):
        eval("self.set_" + stat + "(" + str(amount_to_set) +")")
        
    def thirsty(self):
        return self.water/self.max_water < 0.20

    def hungry(self):
        return self.food/self.max_food < 0.20

    def update_print(self):
        self.stats_surfaces = list()
        str_to_print = "HP: " + str(self.hp) 
        self.stats_surfaces.append(self.font.render(str_to_print, False, (0,0,0,0)))
        str_to_print = "WTR: {:.1f}".format(self.water) + "/" + str(self.max_water)
        self.stats_surfaces.append(self.font.render(str_to_print, False, (0,0,0,0)))
        str_to_print = "FOOD: {:.1f}".format(self.food) + "/" + str(self.max_food)
        self.stats_surfaces.append(self.font.render(str_to_print, False, (0,0,0,0)))
        str_to_print = "SPD: {:.1f}".format(self.speed) 
        self.stats_surfaces.append(self.font.render(str_to_print, False, (0,0,0,0)))
        #str_to_print = self.food_source[:4].upper()
        #self.stats_surfaces.append(self.font.render(str_to_print, False, (0,0,0,0)))
        
        if constants.BUG_FIXING:
            str_to_print = "ID: " + str(self.id) 
            self.stats_surfaces.append(self.font.render(str_to_print, False, (0,0,0,0)))
            (x,y) = self.position_component.position
            str_to_print = str((int(x),int(y))) 
            self.stats_surfaces.append(self.font.render(str_to_print, False, (0,0,0,0)))
    

    def update_stats(self):
        if self.hp == 0:
            return False,None
        finished_step = self.time.frame_counter == self.frames_per_step
        if finished_step:
            if self.water == 0 or self.food == 0:
                self.hp-=1
            if self.water - self.water_consumption_per_step > 0 :
                self.water-=self.water_consumption_per_step
            else:
                self.water = 0
            if self.food - self.food_consumption_per_step > 0 :
                self.food-=self.food_consumption_per_step
            else:
                self.food = 0
        return True,finished_step
    
    def update(self):
        self.frames_per_step = int(constants.FPS/(self.speed + self.temp_speed))
        alive,finished_step = self.update_stats()
        self.update_print()
        self.time.update()
        if finished_step:
            self.time.reset()
        return alive,finished_step

    def draw(self):
        (position_x,position_y) = self.position_component.position
        for i,surface in enumerate(self.stats_surfaces):
            self.display.blit(surface,(position_x*constants.TILESIZE, (position_y+1)*constants.TILESIZE + i*(self.font_size/2 +2)))

