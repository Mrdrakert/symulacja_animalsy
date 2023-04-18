import pygame

GRASS_SIZE = 7

class Grass:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.size = GRASS_SIZE
        self.color = color
        self.width = width
        self.height = height

    def draw(self, screen, offsetx, offsety, scale):
        if int((self.x + offsetx) * scale) > 0 and int((self.y + offsety) * scale) > 0:
            pygame.draw.circle(screen, self.color, (int((self.x + offsetx) * scale), int((self.y + offsety) * scale)), self.size * scale)