import random
import pygame
from Grass import Grass

class Grasses:
    def __init__(self, width, height, color, grass_spawn_cd):
        self.grass_list = []
        self.done = False

        self.width = width
        self.height = height
        self.color = color

        self.grass_spawn_cd = grass_spawn_cd

        for i in range(30):
            self.add_grass(width, height, color)

    def add_grass(self, width, height, color):
        self.grass_list.append(Grass(random.randint(0, width), random.randint(0, height), color))

    def live(self):
        clock = pygame.time.Clock()
        while not self.done:
            self.add_grass(self.width, self.height, self.color)
            clock.tick(self.grass_spawn_cd)