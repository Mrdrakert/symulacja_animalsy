import pygame
import random
import math


# Set up the screen
pygame.init()
WIDTH, HEIGHT = 800, 600
LEFF_MENU_WIDTH = 180
BOTTOM_MENU_HEIGHT = 100
SIM_LEFT, SIM_UP, SIM_RIGHT, SIM_DOWN = LEFF_MENU_WIDTH, 0, WIDTH, HEIGHT - BOTTOM_MENU_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
left_menu = screen.subsurface(pygame.Rect(0,0,LEFF_MENU_WIDTH, HEIGHT))
bottom_menu = screen.subsurface(pygame.Rect(LEFF_MENU_WIDTH, HEIGHT - BOTTOM_MENU_HEIGHT, WIDTH - LEFF_MENU_WIDTH, BOTTOM_MENU_HEIGHT))
simulation = screen.subsurface(pygame.Rect(SIM_LEFT,SIM_UP,SIM_RIGHT - SIM_LEFT, SIM_DOWN - SIM_UP))
pygame.display.set_caption("Animal Simulation")

scale = 1.0
scale_dif = 0.1
offsetx, offsety = 0, 0


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)
ORANGE = (255, 165, 0)
DARKGRAY = (64,64,64)
DARKGREEN = (0, 102, 51)
LIGHTGRAY = (198, 198, 198)

# Set up animals
RABBIT_SIZE = 10
FOX_SIZE = 15
GRASS_SIZE = 7

RABBIT_NUMBER = 50
FOX_NUMBER = 5
GRASS_NUMBER = 100

RABBIT_RADIUS = RABBIT_SIZE * 10
RABBIT_SPEED = 1
FOX_SPEED = 1.3


rabbits = []
foxes = []
grass = []


#Rabbit class
class Rabbit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = RABBIT_SIZE
        self.radius = RABBIT_RADIUS
        self.speed = RABBIT_SPEED
        self.color = GREY
        self.eaten = False

        self.time_to_live = 500
        self.max_time_to_live = 500

        self.saved_direction = (0, 0)
        self.time_going_in_direction = 0
        self.time_to_change_direction = (60, 120)

        self.reproductive_cooldown = 600
        self.reproductive_timer = 0

    def reproduce(self, nearest_rabbit):
        if (self.reproductive_timer <= 0 and nearest_rabbit.reproductive_timer <= 0):
            new_rabbit = Rabbit(self.x, self.y)
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
                self.reproduce(nearest_rabbit)
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
        elif self.x > WIDTH - self.size:
            self.x = WIDTH - self.size

        if self.y < self.size:
            self.y = self.size
        elif self.y > HEIGHT - self.size:
            self.y = HEIGHT - self.size
        

    def eat(self, grass, grass_list):
        grass_list.remove(grass)
        self.time_to_live += self.max_time_to_live
        self.eaten = True

    def draw(self, screen):
        if int((self.x + offsetx) * scale) > 0 and int((self.y + offsety) * scale) > 0:
            pygame.draw.circle(screen, self.color, (int((self.x + offsetx)* scale), int((self.y + offsety) * scale)), self.size * scale)
    
    

#Fox class
class Fox:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = FOX_SIZE
        self.speed = FOX_SPEED
        self.color = ORANGE
        self.eaten = False
        self.reproduce = False

        self.time_to_live = 800
        self.max_time_to_live = 800

    def move(self, rabbits, foxes):
        if self.time_to_live <= 0:
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

        if nearest_rabbit is not None:
            if nearest_distance < self.size + nearest_rabbit.size:
                self.eat(nearest_rabbit, rabbits)
            else:
                self.x += (nearest_rabbit.x - self.x) * self.speed / nearest_distance
                self.y += (nearest_rabbit.y - self.y) * self.speed / nearest_distance

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
        elif self.x > WIDTH - self.size:
            self.x = WIDTH - self.size

        if self.y < self.size:
            self.y = self.size
        elif self.y > HEIGHT - self.size:
            self.y = HEIGHT - self.size

    def eat(self, rabbit, rabbits):
        rabbits.remove(rabbit)
        self.time_to_live = self.max_time_to_live
        self.eaten = True

    def draw(self, screen):
        if int((self.x + offsetx) * scale) > 0 and int((self.y + offsety) * scale) > 0:
            pygame.draw.circle(screen, self.color, (int((self.x + offsetx)* scale), int((self.y + offsety)* scale)), self.size * scale)

    def reproduce(self):
        if self.reproduce:
            foxes.append(Fox(self.x, self.y))
            self.reproduce = False

#Grass class
class Grass:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = GRASS_SIZE
        self.color = GREEN

    def draw(self, screen):
        if int((self.x + offsetx) * scale) > 0 and int((self.y + offsety) * scale) > 0:
            pygame.draw.circle(screen, self.color, (int((self.x + offsetx) * scale), int((self.y + offsety) * scale)), self.size * scale)


# Create animals
for i in range(RABBIT_NUMBER):
    x = random.randrange(RABBIT_SIZE, WIDTH - RABBIT_SIZE)
    y = random.randrange(RABBIT_SIZE, HEIGHT - RABBIT_SIZE)
    rabbits.append(Rabbit(x, y))

for i in range(FOX_NUMBER):
    x = random.randrange(FOX_SIZE, WIDTH - FOX_SIZE)
    y = random.randrange(FOX_SIZE, HEIGHT - FOX_SIZE)
    foxes.append(Fox(x, y))

for i in range(GRASS_NUMBER):
    x = random.randrange(GRASS_SIZE, WIDTH - GRASS_SIZE)
    y = random.randrange(GRASS_SIZE, HEIGHT - GRASS_SIZE)
    grass.append(Grass(x, y))


# Set up game loop
running = True
clock = pygame.time.Clock()
sim_pressed = False

while running:
    # Handle events
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
                scale = scale + scale_dif
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5: #scroll down
            mouse_x, mouse_y = event.pos
            if SIM_LEFT <= mouse_x <= SIM_RIGHT and SIM_UP <= mouse_y <= SIM_DOWN:
                scale = scale - scale_dif
    if sim_pressed:
        mouse_x, mouse_y = event.pos
        offsetx = offsetx - prev_mouse_x + mouse_x
        offsety = offsety - prev_mouse_y + mouse_y
        prev_mouse_x = mouse_x
        prev_mouse_y = mouse_y

    # Clear the screen
    simulation.fill(LIGHTGRAY)
    # Move animals
    for rabbit in rabbits:
        rabbit.move(grass, foxes, rabbits)
        rabbit.draw(simulation)

    for fox in foxes:
        fox.move(rabbits, foxes)
        fox.draw(simulation)

    for g in grass:
        g.draw(simulation)

    #menus
    left_menu.fill(GREY)
    bottom_menu.fill(DARKGRAY)

    # Update the screen
    pygame.display.flip()

    # Wait for the next frame
    clock.tick(60)

# Clean up
pygame.quit()