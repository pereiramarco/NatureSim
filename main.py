#from termcolor import colored
from Creature import Creature
from Game import Game
import aux.constants as constants
import random
import pygame
import time

pygame.display.init()
pygame.font.init()


DISPLAYSURF = pygame.display.set_mode((constants.MAPWIDTH*constants.TILESIZE,constants.MAPHEIGHT*constants.TILESIZE))

pygame.display.set_caption('NatureSim')

game = Game(constants.MAPWIDTH,constants.MAPHEIGHT,DISPLAYSURF)

for id in range(20):
    x = random.randint(0,game.map.width-1)
    y = random.randint(0,game.map.height-1)
    while game.map.grid[y][x] != constants.TILENAMES['grass']:
        x = random.randint(0,game.map.width-1)
        y = random.randint(0,game.map.height-1)
    game.add_creature(Creature(game.time,game.map.grid,DISPLAYSURF,(x,y),"assets/creatures/creature.png",random.randint(10,20),random.randint(50,100),random.randint(0,10)/10+1,id))

running = True

def input(events):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                global running 
                running = False

while running:
    events = pygame.event.get()
    input(events)
    time.sleep(constants.TIMEPERFRAME)
    DISPLAYSURF.fill((0,0,0))
    game.update()
    game.draw()
    pygame.display.flip()

pygame.display.quit()
pygame.font.quit()