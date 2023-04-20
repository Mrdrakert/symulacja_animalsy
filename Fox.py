from time import sleep
import pygame
import random
import math

FOX_SIZE = 12

class Fox:
    def __init__(self, x, y, map_width, map_height, color, speed, life_speed_up = 1):
        self.x = x
        self.y = y
        self.size = FOX_SIZE
        self.speed = speed * life_speed_up
        self.color = color
        self.map_width = map_width
        self.map_height = map_height
        self.done = False

        self.life_speed_up = life_speed_up

        self.time_to_live = 800
        self.max_time_to_live = 800

        self.saved_direction = (0, 0)
        self.time_going_in_direction = 0
        self.time_to_change_direction = (60, 120)

    def pass_time(self, foxes, fox_lock):
        if self.time_to_live <= 0:
            with fox_lock:
                foxes.remove(self)
            return
        else:
            self.time_to_live -= 1 * self.life_speed_up

    def get_rabbit_info(self, rabbits):
        # Move towards rabbits
        nearest_rabbit = None
        nearest_distance = 100000
        for r in rabbits:
            distance = math.sqrt((self.x - r.x)**2 + (self.y - r.y)**2)
            if distance < nearest_distance and r.eaten == False:
                nearest_distance = distance
                nearest_rabbit = r
        return nearest_rabbit, nearest_distance
    
    def hunt_rabbit(self, best_rabbit, best_r_distance):
        if best_rabbit is not None and self.time_to_live < self.max_time_to_live * 0.9:
            if best_r_distance < self.size + best_rabbit.size:
                self.eat(best_rabbit)
            else:
                self.x += (best_rabbit.x - self.x) * self.speed / best_r_distance
                self.y += (best_rabbit.y - self.y) * self.speed / best_r_distance

    def go_randomly(self):
        #pick a direction
        if self.saved_direction == (0, 0):
            self.saved_direction = (random.uniform(-1, 1), random.uniform(-1, 1))
            #normalization
            self.saved_direction = (self.saved_direction[0] / math.sqrt(self.saved_direction[0]**2 + self.saved_direction[1]**2), self.saved_direction[1] / math.sqrt(self.saved_direction[0]**2 + self.saved_direction[1]**2))
            self.time_going_in_direction = random.randint(self.time_to_change_direction[0], self.time_to_change_direction[1])
        
        #move in that direction for time
        self.time_going_in_direction -= 1

        if self.time_going_in_direction > 0:
            self.x += self.saved_direction[0] * self.speed
            self.y += self.saved_direction[1] * self.speed
        else:
            self.saved_direction = (0, 0)

    def get_fox_info(self, foxes):
        nearest_fox = None
        nearest_distance = 100000
        for f in foxes:
            distance = math.sqrt((self.x - f.x)**2 + (self.y - f.y)**2)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_fox = f
        return nearest_fox, nearest_distance
    
    def reproduce(self, foxes):
        #foxes.append(Fox(self.x, self.y))
        pass

    def handle_collisions(self, foxes):
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

    def eat(self, rabbit):
        rabbit.eaten = True
        self.time_to_live += int(self.max_time_to_live/2)
        if self.time_to_live > self.max_time_to_live:
            self.time_to_live = self.max_time_to_live

    def draw(self, screen, offsetx, offsety, scale):
        if int((self.x + offsetx) * scale) > 0 and int((self.y + offsety) * scale) > 0:
            x = int((self.x + offsetx) * scale - self.size * scale) 
            y = int((self.y + offsety) * scale - self.size * scale)
            img = pygame.transform.scale(self.color, (self.size * scale * 2, self.size * scale * 2))
            screen.blit(img ,(x,y))

    def alive(self):
        if self.time_to_live <= 0:
            return False
        else:
            return True

    def action(self, rabbits, foxes, fox_lock):
        self.pass_time(foxes, fox_lock)
        
        best_rabbit, best_r_distance = self.get_rabbit_info(rabbits)

        if best_rabbit is not None and self.time_to_live < self.max_time_to_live * 0.9:
            self.hunt_rabbit(best_rabbit, best_r_distance)
        else:
            self.go_randomly()

        best_fox, best_f_distance = self.get_fox_info(foxes)

        if best_fox is not None:
            if best_f_distance < self.size + best_fox.size:
                self.reproduce(foxes)

        self.handle_collisions(foxes)
    
    def live(self, foxes, rabbits, fox_lock, clock_speed):
        clock = pygame.time.Clock()
        while self.alive() and not self.done:
            self.action(rabbits, foxes, fox_lock)
            clock.tick(clock_speed)