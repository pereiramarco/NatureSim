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
    hp = random.randint(10,20)
    starting_water = random.randint(50,100)
    water_consumption = random.randint(5,100)/100
    starting_food = random.randint(50,100)
    food_consumption = random.randint(5,100)/100
    food_source = random.choice(list(constants.FOOD_TYPES.keys()))
    speed = random.randint(0,10)/10+1
    vision = 1+random.randint(0,4)
    sprite_location = "assets/creatures/creature_" + food_source + ".png"
    game.add_creature(DISPLAYSURF,(x,y),sprite_location,food_source,hp,starting_water,water_consumption,starting_food,food_consumption,speed,vision,id,"he")

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