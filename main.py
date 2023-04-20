import pygame
import random
import math
from threading import Thread
from threading import Lock
from Fox import Fox
from Rabbit import Rabbit
from Grass import Grass
from Grasses import Grasses
import os


# Set up the screen
pygame.init()
WIDTH, HEIGHT = 1000, 600
LEFF_MENU_WIDTH = 180
BOTTOM_MENU_HEIGHT = 100
SIM_LEFT, SIM_UP, SIM_RIGHT, SIM_DOWN = LEFF_MENU_WIDTH, 0, WIDTH, HEIGHT - BOTTOM_MENU_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
left_menu = screen.subsurface(pygame.Rect(0,0,LEFF_MENU_WIDTH, HEIGHT))
bottom_menu = screen.subsurface(pygame.Rect(LEFF_MENU_WIDTH, HEIGHT - BOTTOM_MENU_HEIGHT, WIDTH - LEFF_MENU_WIDTH, BOTTOM_MENU_HEIGHT))
simulation = screen.subsurface(pygame.Rect(SIM_LEFT,SIM_UP,SIM_RIGHT - SIM_LEFT, SIM_DOWN - SIM_UP))
pygame.display.set_caption("Animal Simulation")

scale = 0.8
scale_dif = 0.1
offsetx, offsety = 10, 10

grassimg = pygame.image.load(os.path.join("grass.png"))
grassimg.convert()

foximg = pygame.image.load(os.path.join("fox.png"))
foximg.convert()

rabbitimg = pygame.image.load(os.path.join("rabbit.png"))
rabbitimg.convert()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)
ORANGE = (255, 165, 0)
DARKGRAY = (64,64,64)
DARKGREEN = (0, 102, 51)
LIGHTGRAY = (198, 198, 198)

# Set up animals
RABBIT_SIZE = 10
FOX_SIZE = 15
GRASS_SIZE = 7

RABBIT_NUMBER = 50
FOX_NUMBER = 5
GRASS_NUMBER = 100

RABBIT_RADIUS = RABBIT_SIZE * 10
RABBIT_SPEED = 1
FOX_SPEED = 1.3

clock_speed = 60
drawing = True

rabbits = []
foxes = []

rabbit_lock = Lock()
fox_lock = Lock()
grass_lock = Lock()

grasses = Grasses(WIDTH, HEIGHT, grassimg, 15)

Thread(target = grasses.live, args = ()).start()

# Create animals
for i in range(RABBIT_NUMBER):
    x = random.randrange(RABBIT_SIZE, WIDTH - RABBIT_SIZE)
    y = random.randrange(RABBIT_SIZE, HEIGHT - RABBIT_SIZE)
    rabbit = Rabbit(x, y, WIDTH, HEIGHT, rabbitimg)
    rabbits.append(rabbit)
    Thread(target = rabbit.live, args = (grasses.grass_list, foxes, rabbits, rabbit_lock, grass_lock, clock_speed)).start()

for i in range(FOX_NUMBER):
    x = random.randrange(FOX_SIZE, WIDTH - FOX_SIZE)
    y = random.randrange(FOX_SIZE, HEIGHT - FOX_SIZE)
    fox = Fox(x, y, WIDTH, HEIGHT, foximg)
    foxes.append(fox)
    Thread(target = fox.live, args = (foxes, rabbits, fox_lock, clock_speed)).start()




# Set up game loop
running = True
clock = pygame.time.Clock()
sim_pressed = False

while running:
    # Handle events
    if (drawing == False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for left mouse button click
                # Check if mouse click is within the bounds of the surface
                mouse_x, mouse_y = event.pos
                # Check if mouse click is within the bounds of the surface
                if SIM_LEFT <= mouse_x <= SIM_RIGHT and SIM_UP <= mouse_y <= SIM_DOWN:
                    sim_pressed = True
                    prev_mouse_x = mouse_x
                    prev_mouse_y = mouse_y
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Check for left mouse button release
                sim_pressed = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4: #scroll up
                mouse_x, mouse_y = event.pos
                if SIM_LEFT <= mouse_x <= SIM_RIGHT and SIM_UP <= mouse_y <= SIM_DOWN:
                    scale = scale + scale_dif
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5: #scroll down
                mouse_x, mouse_y = event.pos
                if SIM_LEFT <= mouse_x <= SIM_RIGHT and SIM_UP <= mouse_y <= SIM_DOWN:
                    scale = scale - scale_dif
        if sim_pressed:
            mouse_x, mouse_y = event.pos
            offsetx = offsetx - prev_mouse_x + mouse_x
            offsety = offsety - prev_mouse_y + mouse_y
            prev_mouse_x = mouse_x
            prev_mouse_y = mouse_y

    if (drawing):
        simulation.fill(LIGHTGRAY)
        pygame.draw.rect(simulation, DARKGREEN, pygame.Rect(int(offsetx * scale), int(offsety * scale), int(WIDTH * scale), int(HEIGHT * scale)))

        for grass in grasses.grass_list:
            grass.draw(simulation, offsetx, offsety, scale)

    for rabbit in rabbits:
        if rabbit.alive() == False:
            rabbits.remove(rabbit)
        else:
            if (drawing):
                rabbit.draw(simulation, offsetx, offsety, scale)

    for fox in foxes:
        if fox.alive() == False:
            foxes.remove(fox)
        else:
            if (drawing):
                fox.draw(simulation, offsetx, offsety, scale)

    if (drawing):
        left_menu.fill(GREY)
        bottom_menu.fill(DARKGRAY)

        pygame.display.flip()

    #print("Frame: ", len(rabbits), len(foxes))
          
    clock.tick(clock_speed)

grasses.done = True
for rabbit in rabbits:
    rabbit.done = True
for fox in foxes:
    fox.done = True

pygame.quit()