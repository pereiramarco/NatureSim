from Components.component import Component

class Position_Component(Component):
    position : tuple

    def __init__(self,position):
        self.position = position

    def update(self,position):
        self.position = position

    def round(self):
        self.position = tuple(round(itup) for itup in self.position)