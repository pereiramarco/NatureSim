

class Time:
    frame_counter : int

    def __init__(self):
        self.frame_counter = 0

    def reset(self):
        self.frame_counter = 0

    def update(self):
        self.frame_counter+=1