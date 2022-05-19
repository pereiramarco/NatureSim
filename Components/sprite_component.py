from Components.position_component import Position_Component
from Components.component import Component
import aux.constants as constants
import pygame

class Sprite_Component(Component):
    sprite : pygame.Surface
    original_sprite : pygame.Surface
    display : pygame.Surface
    size : list
    position_component : Position_Component

    def __init__(self, display, location, position_component, size_multiplier = 1):
        self.display = display
        self.sprite = self.original_sprite = pygame.image.load(location)
        self.size = self.sprite.get_size()
        self.position_component = position_component
        self.scale_sprite(size_multiplier)

    def scale_sprite(self,size_multiplier):
        self.sprite = pygame.transform.scale(self.original_sprite, (int(self.size[0]*size_multiplier), int(self.size[1]*size_multiplier)))
        
    def draw(self):
        (position_x,position_y) = self.position_component.position
        self.display.blit(self.sprite,(position_x*constants.TILESIZE, position_y*constants.TILESIZE))