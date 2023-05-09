import random
import math
from time import sleep
import time
import pygame
from threading import Thread

RABBIT_SIZE = 8
RABBIT_NUMBER = 50
RABBIT_RADIUS = RABBIT_SIZE * 10

class Rabbit:
    def __init__(self, x, y, map_width, map_height, color, speed, life_speed_up, children_count, reproductive, life):
        self.x = x
        self.y = y
        self.size = RABBIT_SIZE
        self.radius = RABBIT_RADIUS
        self.speed = speed * life_speed_up
        self.color = color
        self.eaten = False
        self.done = False
        self.children_count = children_count
        self.drawing = True

        self.sex = random.choice(['m', 'f'])

        self.life_speed_up = life_speed_up

        self.map_width = map_width
        self.map_height = map_height

        self.time_to_live = life
        self.max_time_to_live = self.time_to_live

        self.saved_direction = (0, 0)
        self.time_going_in_direction = 0
        self.time_to_change_direction = (60, 120)

        self.reproductive_cooldown = reproductive
        self.cooldown_first = reproductive
        self.reproductive_cooldown -= random.randint(0, 100)
        self.reproductive_timer = self.reproductive_cooldown

    def reproduce(self, nearest_rabbit, rabbits, grass, foxes, rabbit_lock, grass_lock, clock_speed):
        if (self.reproductive_timer <= 0 and nearest_rabbit.reproductive_timer <= 0 and self.alive() and nearest_rabbit.alive()):
            nearest_rabbit.reproductive_timer = nearest_rabbit.reproductive_cooldown
            self.reproductive_timer = self.reproductive_cooldown
            for _ in range(self.children_count):
                new_rabbit = Rabbit(self.x, self.y, self.map_width, self.map_height, self.color, self.speed/self.life_speed_up, self.life_speed_up, self.children_count, self.cooldown_first, self.max_time_to_live)
                new_rabbit.reproductive_timer = new_rabbit.reproductive_cooldown
                new_rabbit.time_to_live = 2* new_rabbit.max_time_to_live / 3
                #with rabbit_lock:
                rabbits.append(new_rabbit)
                self.threads[new_rabbit] = Thread(target = new_rabbit.live, args = (grass, foxes, rabbits, self.threads, rabbit_lock, grass_lock, clock_speed, self.drawing))
                self.threads[new_rabbit].start()
            

    def pass_time(self, rabbits, rabbit_lock):
        if self.time_to_live <= 0:
            with rabbit_lock:
                rabbits.done = True
            return
        else:
            self.time_to_live -= 1 * self.life_speed_up

        if self.reproductive_timer > 0:
            self.reproductive_timer -= 1 * self.life_speed_up

    def get_grass_info(self, grass):
        nearest_grass = None
        nearest_g_distance = 100000
        for g in grass:
            distance = math.sqrt((self.x - g.x)**2 + (self.y - g.y)**2)
            if distance < nearest_g_distance:
                nearest_g_distance = distance
                nearest_grass = g

        return nearest_grass, nearest_g_distance
    
    def get_fox_info(self, foxes):
        nearest_fox = None
        nearest_f_distance = 100000
        for f in foxes:
            distance = math.sqrt((self.x - f.x)**2 + (self.y - f.y)**2)
            if distance < nearest_f_distance:
                nearest_f_distance = distance
                nearest_fox = f
        
        return nearest_fox, nearest_f_distance
    
    def get_rabbit_info(self, rabbits):
        nearest_rabbit = None
        nearest_r_distance = 100000
        for r in rabbits:
            distance = math.sqrt((self.x - r.x)**2 + (self.y - r.y)**2)
            if distance < nearest_r_distance and r is not self and r.reproductive_timer <= 0 and r.sex != self.sex:
                nearest_r_distance = distance
                nearest_rabbit = r

        return nearest_rabbit, nearest_r_distance
    
    def run_from_fox(self, nearest_fox, nearest_f_distance):
        if nearest_f_distance != 0:
            self.x -= (nearest_fox.x - self.x) * self.speed / nearest_f_distance
            self.y -= (nearest_fox.y - self.y) * self.speed / nearest_f_distance

    def hunt_grass(self, nearest_grass, nearest_g_distance, grass, grass_lock):
        if nearest_g_distance < self.size + nearest_grass.size:
                self.eat(nearest_grass, grass, grass_lock)
        else:
            self.x += (nearest_grass.x - self.x) * self.speed / nearest_g_distance
            self.y += (nearest_grass.y - self.y) * self.speed / nearest_g_distance
    
    def find_partner(self, best_rabbit, best_r_distance, rabbits, grass, foxes, rabbit_lock, grass_lock, clock_speed):
        if best_r_distance < self.size + best_rabbit.size + 1:
                self.reproduce(best_rabbit, rabbits, grass, foxes, rabbit_lock, grass_lock, clock_speed)
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

    def handle_collisions(self, rabbits):
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

    def eat(self, grass, grass_list, grass_lock):
        with grass_lock:
            grass_list.remove(grass)
        self.time_to_live += int(self.max_time_to_live/3)
        if self.time_to_live > self.max_time_to_live:
            self.time_to_live = self.max_time_to_live

    def draw(self, screen, offsetx, offsety, scale):
        if int((self.x + offsetx) * scale) > 0 and int((self.y + offsety) * scale) > 0:
            x = int((self.x + offsetx) * scale - self.size * scale) 
            y = int((self.y + offsety) * scale - self.size * scale)
            img = pygame.transform.scale(self.color, (self.size * scale * 2, self.size * scale * 2))
            if (self.sex == 'f'):
                img.fill((240, 173, 200), special_flags=pygame.BLEND_RGB_MULT)
            else:
                img.fill((178, 200, 240), special_flags=pygame.BLEND_RGB_MULT)
            screen.blit(img ,(x,y))
    
    def alive(self):
        if self.time_to_live <= 0 or self.eaten or self.done:
            return False
        else:
            return True
        
    def action(self, grass, foxes, rabbits, rabbit_lock, grass_lock, clock_speed):
        self.pass_time(rabbits, rabbit_lock)

        nearest_grass, nearest_g_distance = self.get_grass_info(grass)
        nearest_fox, nearest_f_distance = self.get_fox_info(foxes)
        best_rabbit, best_r_distance = self.get_rabbit_info(rabbits)

        if nearest_fox is not None and nearest_f_distance < self.radius:
            self.run_from_fox(nearest_fox, nearest_f_distance)
        elif nearest_grass is not None and nearest_g_distance < self.radius and self.time_to_live < 400:
            self.hunt_grass(nearest_grass, nearest_g_distance, grass, grass_lock)
        elif best_rabbit is not None and best_r_distance < self.radius and self.reproductive_timer <= 0:
            self.find_partner(best_rabbit, best_r_distance, rabbits, grass, foxes, rabbit_lock, grass_lock, clock_speed)
        else:
            self.go_randomly()

        self.handle_collisions(rabbits)

    def live(self, grass, foxes, rabbits, threads, rabbits_lock, grass_lock, clock_speed, drawing):
        self.drawing = drawing
        self.threads = threads
        if drawing:
            clock = pygame.time.Clock()
        if len(rabbits) < 120:
            while self.alive() and not self.done:
                self.action(grass, foxes, rabbits, rabbits_lock, grass_lock, clock_speed)

                if drawing:
                    clock.tick(clock_speed)
                else:
                    time.sleep(1/clock_speed)
        else:
            self.done = True

