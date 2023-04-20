import pygame
import random
import os
from threading import Thread
from threading import Lock
from Fox import Fox
from Rabbit import Rabbit
from Grasses import Grasses

WIDTH, HEIGHT = 1000, 600
LEFF_MENU_WIDTH = 180
BOTTOM_MENU_HEIGHT = 100
SIM_LEFT, SIM_UP, SIM_RIGHT, SIM_DOWN = LEFF_MENU_WIDTH, 0, WIDTH, HEIGHT - BOTTOM_MENU_HEIGHT

GRAY = (128, 128, 128)
DARKGRAY = (64,64,64)
DARKGREEN = (0, 102, 51)
LIGHTGRAY = (198, 198, 198)

RABBIT_SIZE = 8
FOX_SIZE = 12

RABBIT_NUMBER = 50
FOX_NUMBER = 10
GRASS_NUMBER = 100

RABBIT_SPEED = 0.8
FOX_SPEED = 1.1

class Simulation():
    def __init__(self, clock_speed = 60, life_speed_up = 1, draw = True):
        self.life_speed_up = life_speed_up
        self.ticks_lived = 0
        # Set up the screen
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.left_menu = self.screen.subsurface(pygame.Rect(0,0,LEFF_MENU_WIDTH, HEIGHT))
        self.bottom_menu = self.screen.subsurface(pygame.Rect(LEFF_MENU_WIDTH, HEIGHT - BOTTOM_MENU_HEIGHT, WIDTH - LEFF_MENU_WIDTH, BOTTOM_MENU_HEIGHT))
        self.simulation = self.screen.subsurface(pygame.Rect(SIM_LEFT,SIM_UP,SIM_RIGHT - SIM_LEFT, SIM_DOWN - SIM_UP))
        pygame.display.set_caption("Animal Simulation")

        self.scale = 0.8
        self.scale_dif = 0.1
        self.offsetx, self.offsety = 10, 10

        self.grassimg = pygame.image.load(os.path.join("grass.png"))
        self.grassimg.convert()

        self.foximg = pygame.image.load(os.path.join("fox.png"))
        self.foximg.convert()

        self.rabbitimg = pygame.image.load(os.path.join("rabbit.png"))
        self.rabbitimg.convert()

        self.clock_speed = clock_speed
        self.drawing = draw

        self.rabbits = []
        self.foxes = []

        self.rabbit_lock = Lock()
        self.fox_lock = Lock()
        self.grass_lock = Lock()

    def run(self):
        grasses = Grasses(WIDTH, HEIGHT, self.grassimg, self.clock_speed/4, self.life_speed_up)
        Thread(target = grasses.live, args = ()).start()

        # Create animals
        for i in range(RABBIT_NUMBER):
            x = random.randrange(RABBIT_SIZE, WIDTH - RABBIT_SIZE)
            y = random.randrange(RABBIT_SIZE, HEIGHT - RABBIT_SIZE)
            rabbit = Rabbit(x, y, WIDTH, HEIGHT, self.rabbitimg, RABBIT_SPEED, self.life_speed_up)
            self.rabbits.append(rabbit)
            Thread(target = rabbit.live, args = (grasses.grass_list, self.foxes, self.rabbits, self.rabbit_lock, self.grass_lock, self.clock_speed)).start()

        for i in range(FOX_NUMBER):
            x = random.randrange(FOX_SIZE, WIDTH - FOX_SIZE)
            y = random.randrange(FOX_SIZE, HEIGHT - FOX_SIZE)
            fox = Fox(x, y, WIDTH, HEIGHT, self.foximg, FOX_SPEED, self.life_speed_up)
            self.foxes.append(fox)
            Thread(target = fox.live, args = (self.foxes, self.rabbits, self.fox_lock, self.clock_speed)).start()

        # Set up game loop
        running = True
        clock = pygame.time.Clock()
        sim_pressed = False

        while running:
            self.ticks_lived += 1

            # Handle events
            if (self.drawing == False):
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
                            self.scale = self.scale + self.scale_dif
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5: #scroll down
                        mouse_x, mouse_y = event.pos
                        if SIM_LEFT <= mouse_x <= SIM_RIGHT and SIM_UP <= mouse_y <= SIM_DOWN:
                            self.scale = self.scale - self.scale_dif
                if sim_pressed:
                    mouse_x, mouse_y = event.pos
                    self.offsetx = self.offsetx - prev_mouse_x + mouse_x
                    self.offsety = self.offsety - prev_mouse_y + mouse_y
                    prev_mouse_x = mouse_x
                    prev_mouse_y = mouse_y

            if (self.drawing):
                self.simulation.fill(LIGHTGRAY)
                pygame.draw.rect(self.simulation, DARKGREEN, pygame.Rect(int(self.offsetx * self.scale), int(self.offsety * self.scale), int(WIDTH * self.scale), int(HEIGHT * self.scale)))

                for grass in grasses.grass_list:
                    grass.draw(self.simulation, self.offsetx, self.offsety, self.scale)

            for rabbit in self.rabbits:
                if rabbit.alive() == False:
                    self.rabbits.remove(rabbit)
                else:
                    if (self.drawing):
                        rabbit.draw(self.simulation, self.offsetx, self.offsety, self.scale)

            for fox in self.foxes:
                if fox.alive() == False:
                    self.foxes.remove(fox)
                else:
                    if (self.drawing):
                        fox.draw(self.simulation, self.offsetx, self.offsety, self.scale)

            if (self.drawing):
                self.left_menu.fill(GRAY)
                self.bottom_menu.fill(DARKGRAY)

                pygame.display.flip()

            clock.tick(self.clock_speed)

            #end criteria)
            if (len(self.rabbits) == 0 or len(self.foxes) == 0):
                running = False

        grasses.done = True
        for rabbit in self.rabbits:
            rabbit.done = True
        for fox in self.foxes:
            fox.done = True

        pygame.quit()

        return self.ticks_lived