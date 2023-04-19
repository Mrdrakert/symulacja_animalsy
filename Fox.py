import pygame
import random
import math

FOX_SIZE = 15
FOX_SPEED = 1.3

class Fox:
    def __init__(self, x, y, map_width, map_height, color):
        self.x = x
        self.y = y
        self.size = FOX_SIZE
        self.speed = FOX_SPEED
        self.color = color
        self.map_width = map_width
        self.map_height = map_height
        self.reproduce = False
        self.done = False

        self.time_to_live = 800
        self.max_time_to_live = 800

        self.saved_direction = (0, 0)
        self.time_going_in_direction = 0
        self.time_to_change_direction = (60, 120)

    def move(self, rabbits, foxes, fox_lock):
        if self.time_to_live <= 0:
            with fox_lock:
                foxes.remove(self)
            return
        else:
            self.time_to_live -= 1


        # Move towards rabbits
        nearest_rabbit = None
        nearest_distance = 100000
        for r in rabbits:
            distance = math.sqrt((self.x - r.x)**2 + (self.y - r.y)**2)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_rabbit = r

        if nearest_rabbit is not None and self.time_to_live < self.max_time_to_live * 0.8:
            if nearest_distance < self.size + nearest_rabbit.size:
                self.eat(nearest_rabbit, rabbits)
            else:
                self.x += (nearest_rabbit.x - self.x) * self.speed / nearest_distance
                self.y += (nearest_rabbit.y - self.y) * self.speed / nearest_distance
        else:
            #pick a direction
            if self.saved_direction == (0, 0):
                self.saved_direction = (random.uniform(-1, 1), random.uniform(-1, 1))
                self.time_going_in_direction = random.randint(self.time_to_change_direction[0], self.time_to_change_direction[1])
            
            #move in that direction for time
            self.time_going_in_direction -= 1

            if self.time_going_in_direction > 0:
                self.x += self.saved_direction[0] * self.speed
                self.y += self.saved_direction[1] * self.speed
            else:
                self.saved_direction = (0, 0)

        # Reproduce
        nearest_fox = None
        nearest_distance = 100000
        for f in foxes:
            distance = math.sqrt((self.x - f.x)**2 + (self.y - f.y)**2)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_fox = f

        if nearest_fox is not None:
            if nearest_distance < self.size + nearest_fox.size:
                self.reproduce = True
            else:
                self.reproduce = False

        # Not collide with each other
        for f in foxes:
            if f is not self:
                distance = math.sqrt((self.x - f.x)**2 + (self.y - f.y)**2)
                if distance < self.size+f.size:
                    if (distance != 0):
                        self.x -= (f.x - self.x) * self.speed / distance
                        self.y -= (f.y - self.y) * self.speed / distance
                    else:
                        #jitter randomly
                        self.x += random.uniform(-1, 1) * self.speed
                        self.y += random.uniform(-1, 1) * self.speed

        # Not go out of the window
        if self.x < self.size:
            self.x = self.size
        elif self.x > self.map_width - self.size:
            self.x = self.map_width - self.size

        if self.y < self.size:
            self.y = self.size
        elif self.y > self.map_height - self.size:
            self.y = self.map_height - self.size

    def eat(self, rabbit, rabbits):
        rabbit.eaten = True
        self.time_to_live = self.max_time_to_live

    def draw(self, screen, offsetx, offsety, scale):
        if int((self.x + offsetx) * scale) > 0 and int((self.y + offsety) * scale) > 0:
            x = int((self.x + offsetx) * scale - self.size * scale) 
            y = int((self.y + offsety) * scale - self.size * scale)
            img = pygame.transform.scale(self.color, (self.size * scale * 2, self.size * scale * 2))
            screen.blit(img ,(x,y))

    def reproduce(self, foxes):
        if self.reproduce:
            foxes.append(Fox(self.x, self.y))
            self.reproduce = False

    def alive(self):
        if self.time_to_live <= 0:
            return False
        else:
            return True
    
    def live(self, foxes, rabbits, fox_lock):
        clock = pygame.time.Clock()
        while self.alive() and not self.done:
            self.move(rabbits, foxes, fox_lock)
            clock.tick(60)