from Components.position_component import Position_Component
from Components.component import Component
import aux.constants as constants
import pygame

class Sprite_Component(Component):
    sprite : pygame.Surface
    display : pygame.Surface
    position_component : Position_Component

    def __init__(self, display, location, position_component):
        self.display = display
        self.sprite = pygame.image.load(location)
        self.position_component = position_component

    def draw(self):
        (position_x,position_y) = self.position_component.position
        self.display.blit(self.sprite,(position_x*constants.TILESIZE, position_y*constants.TILESIZE))