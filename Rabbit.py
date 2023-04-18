import random
import math
import pygame

RABBIT_SIZE = 10
RABBIT_NUMBER = 50
RABBIT_RADIUS = RABBIT_SIZE * 10
RABBIT_SPEED = 1

class Rabbit:
    def __init__(self, x, y, map_width, map_height, color):
        self.x = x
        self.y = y
        self.size = RABBIT_SIZE
        self.radius = RABBIT_RADIUS
        self.speed = RABBIT_SPEED
        self.color = color
        self.eaten = False

        self.map_width = map_width
        self.map_height = map_height

        self.time_to_live = 500
        self.max_time_to_live = 500

        self.saved_direction = (0, 0)
        self.time_going_in_direction = 0
        self.time_to_change_direction = (60, 120)

        self.reproductive_cooldown = 600
        self.reproductive_timer = 0

    def reproduce(self, nearest_rabbit, rabbits):
        if (self.reproductive_timer <= 0 and nearest_rabbit.reproductive_timer <= 0):
            new_rabbit = Rabbit(self.x, self.y, self.map_width, self.map_height, self.color)
            new_rabbit.reproductive_timer = new_rabbit.reproductive_cooldown
            rabbits.append(new_rabbit)
            nearest_rabbit.reproductive_timer = nearest_rabbit.reproductive_cooldown
            self.reproductive_timer = self.reproductive_cooldown

    def move(self, grass, foxes, rabbits):
        if self.time_to_live <= 0:
            rabbits.remove(self)
            return
        else:
            self.time_to_live -= 1

        if self.reproductive_timer > 0:
            self.reproductive_timer -= 1

        # Move towards grass
        nearest_grass = None
        nearest_g_distance = 100000
        for g in grass:
            distance = math.sqrt((self.x - g.x)**2 + (self.y - g.y)**2)
            if distance < nearest_g_distance:
                nearest_g_distance = distance
                nearest_grass = g

        # Move away from foxes
        nearest_fox = None
        nearest_f_distance = 100000
        for f in foxes:
            distance = math.sqrt((self.x - f.x)**2 + (self.y - f.y)**2)
            if distance < nearest_f_distance:
                nearest_f_distance = distance
                nearest_fox = f

        # Reproduce
        nearest_rabbit = None
        nearest_r_distance = 100000
        for r in rabbits:
            distance = math.sqrt((self.x - r.x)**2 + (self.y - r.y)**2)
            if distance < nearest_r_distance and r is not self and r.reproductive_timer <= 0:
                nearest_r_distance = distance
                nearest_rabbit = r

        # choose what to do
        if nearest_fox is not None and nearest_f_distance < self.radius:
            if nearest_f_distance != 0:
                self.x -= (nearest_fox.x - self.x) * self.speed / nearest_f_distance
                self.y -= (nearest_fox.y - self.y) * self.speed / nearest_f_distance
        elif nearest_grass is not None and nearest_g_distance < self.radius:
            if nearest_g_distance < self.size + nearest_grass.size:
                self.eat(nearest_grass, grass)
            else:
                self.x += (nearest_grass.x - self.x) * self.speed / nearest_g_distance
                self.y += (nearest_grass.y - self.y) * self.speed / nearest_g_distance
        elif nearest_rabbit is not None and nearest_r_distance < self.radius and self.reproductive_timer <= 0:
            if nearest_r_distance < self.size + nearest_rabbit.size + 1:
                self.reproduce(nearest_rabbit, rabbits)
            else:
                self.x += (nearest_rabbit.x - self.x) * self.speed / nearest_r_distance
                self.y += (nearest_rabbit.y - self.y) * self.speed / nearest_r_distance
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
            

        # Not collide with each other
        for r in rabbits:
            if r is not self:
                distance = math.sqrt((self.x - r.x)**2 + (self.y - r.y)**2)
                if distance < self.size+r.size:
                    if (distance != 0):
                        self.x -= (r.x - self.x) * self.speed / distance
                        self.y -= (r.y - self.y) * self.speed / distance
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
        

    def eat(self, grass, grass_list):
        grass_list.remove(grass)
        self.time_to_live += self.max_time_to_live
        self.eaten = True

    def draw(self, screen, offsetx, offsety, scale):
        if int((self.x + offsetx) * scale) > 0 and int((self.y + offsety) * scale) > 0:
            pygame.draw.circle(screen, self.color, (int((self.x + offsetx)* scale), int((self.y + offsety) * scale)), self.size * scale)