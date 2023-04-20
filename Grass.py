import pygame

GRASS_SIZE = 6

class Grass:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.size = GRASS_SIZE
        self.color = color

    def draw(self, screen, offsetx, offsety, scale):
        if int((self.x + offsetx) * scale) > 0 and int((self.y + offsety) * scale) > 0:
            x = int((self.x + offsetx) * scale - self.size * scale) 
            y = int((self.y + offsety) * scale - self.size * scale)
            img = pygame.transform.scale(self.color, (self.size * scale * 2.5, self.size * scale * 2.5))
            screen.blit(img ,(x,y))