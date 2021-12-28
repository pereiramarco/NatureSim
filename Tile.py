from Components.position_component import Position_Component
from Components.sprite_component import Sprite_Component

class Tile:
    sprite_component : Sprite_Component
    position_component : Position_Component

    def __init__(self,position_component,sprite_component):
        self.sprite_component = sprite_component
        self.position_component = position_component

    def draw(self):
        self.sprite_component.draw()
