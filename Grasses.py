import random
import pygame
from Grass import Grass

class Grasses:
    def __init__(self):
        self.grass_list = []
        self.done = False

    def add_grass(self, width, height, color):
        self.grass_list.append(Grass(random.randint(0, width), random.randint(0, height), width, height, color))

    def live(self, width, height, color):
        clock = pygame.time.Clock()
        while not self.done:
            self.add_grass(width, height, color)
            clock.tick(12)