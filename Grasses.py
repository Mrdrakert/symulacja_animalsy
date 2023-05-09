import random
from Grass import Grass
import time

class Grasses:
    def __init__(self, width, height, color, grass_spawn_cd, life_speed_up = 1):
        self.grass_list = []
        self.done = False

        self.width = width
        self.height = height
        self.color = color

        self.grass_spawn_cd = grass_spawn_cd * life_speed_up

        for i in range(30):
            self.add_grass(width, height, color)

    def add_grass(self, width, height, color):
        if len(self.grass_list) > 100:
            return
        self.grass_list.append(Grass(random.randint(0, width), random.randint(0, height), color))

    def live(self):
        while not self.done:
            self.add_grass(self.width, self.height, self.color)
            time.sleep(1/self.grass_spawn_cd)