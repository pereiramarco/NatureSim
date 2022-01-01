from Tile import Tile
import aux.constants as constants
import pygame

class Temporary_Tile(Tile):
    hitpoints : int

    def __init__(self,position_component,sprite_component,hitpoints):
        super().__init__(position_component,sprite_component)
        self.hitpoints = hitpoints

    def update(self):
        if self.hitpoints==0:
            return "FINISHED"

    def remove_hitpoints(self,amount_to_remove):
        self.hitpoints -= amount_to_remove
    
    def draw(self):
        super().draw()
        #(position_x,position_y) = self.position_component.position
        #str_to_print = "HP: {:.1f}".format(self.hitpoints) 
        #font = pygame.font.SysFont("Comic Sans", 20)
        #surface = font.render(str_to_print, False, (0,0,0,0))
        #self.sprite_component.display.blit(surface,(position_x*constants.TILESIZE, (position_y)*constants.TILESIZE))
