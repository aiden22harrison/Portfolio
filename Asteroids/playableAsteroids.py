import pygame
import os
import math
import random
pygame.font.init()

WIDTH, HEIGHT = (1000, 1000)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

SHIPWIDTH, SHIPHEIGHT = (30,50)
BULLETWIDTH, BULLETHEIGHT = (5,10)

ASTEROIDWIDTH, ASTEROIDHEIGHT = (75, 75)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

SHIP_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Ship.png')), (SHIPWIDTH, SHIPHEIGHT))

BULLET_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bullet.png')), (BULLETWIDTH, BULLETHEIGHT))

ASTEROID_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Astroid1.png')), (ASTEROIDWIDTH, ASTEROIDHEIGHT)), 
                pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Astroid2.png')), (ASTEROIDWIDTH, ASTEROIDHEIGHT)),
                pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Astroid3.png')), (ASTEROIDWIDTH, ASTEROIDHEIGHT))]

class Ship:
    ROT_VEL = 3
    TILT_CORRECTION = 90
    ACCEL = 0.15
    DEACCEL = 0.05
    VEL_CAP = 5
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = SHIP_IMG
        self.tilt = 0
        self.vel = 0.05
        self.tick_count = 1
        self.radians_x = 0
        self.radians_y = 0
        self.reset = False
    
    def ship_movement(self, keys_pressed):
        if keys_pressed[pygame.K_w]:
            if self.reset == True:
                self.reset = False
                self.vel = self.vel/self.tick_count
            self.vel += self.ACCEL
            self.rad_to_offset(math.radians(self.tilt + self.TILT_CORRECTION), self.vel)
            self.x += self.radians_x
            self.y -= self.radians_y
            if self.vel > self.VEL_CAP:
                self.vel = self.VEL_CAP
            self.tick_count = 1
            
        if not keys_pressed[pygame.K_w]:
            if self.reset == False:
                self.rad_to_offset(math.radians(self.tilt + self.TILT_CORRECTION), self.vel)
                self.reset = True
            self.x += self.radians_x/self.tick_count
            self.y -= self.radians_y/self.tick_count
            self.tick_count += self.DEACCEL
            if self.vel <= 0:
                self.vel = 0

        if keys_pressed[pygame.K_a]:
            self.tilt += self.ROT_VEL
            if self.tilt <= 0 and self.tilt >= 360:
                self.tilt -= self.ROT_VEL
            elif self.tilt < 0:
                self.tilt = 360
            elif self.tilt > 360:
                self.tilt = 0
            self.last_turn = 0
            self.turn_tick_count = 1

        if keys_pressed[pygame.K_d]:
            self.tilt -= self.ROT_VEL
            if self.tilt <= 0 and self.tilt >= 360:
                self.tilt -= self.ROT_VEL
            elif self.tilt < 0:
                self.tilt = 360
            elif self.tilt > 360:
                self.tilt = 0
            self.last_turn = 1
            self.turn_tick_count = 1
        self.detect_border()

    def detect_border(self):
        if self.x <= -25:
            self.x = 1025
        elif self.x >= 1025:
            self.x = -25
        elif self.y <= -25:
            self.y = 1025
        elif self.y >= 1025:
            self.y = -25

    def draw(self):
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)
        WIN.blit(rotated_image, new_rect.topleft)

    def rad_to_offset(self, radians, offset):
        x = math.cos(radians) * offset
        y = math.sin(radians) * offset
        self.radians_x = x
        self.radians_y = y

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Bullet(Ship):
    VELOCITY = 10
    TILT_CORRECTION = 90
    def __init__(self, Ship, bullets):
        self.x = Ship.x + SHIPWIDTH/2
        self.y = Ship.y + SHIPHEIGHT/2
        self.tilt = Ship.tilt
        self.img = BULLET_IMG
        self.radiants_x = 0
        self.radians_y = 0
        self.tick_count = 0
        self.bullets = bullets
        self.remove_cooldown = 70

    def draw(self): 
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)
        WIN.blit(rotated_image, new_rect.topleft)
        self.move_bullet()
        self.detect_border()
        self.remove_bullet()


    def move_bullet(self):
        self.rad_to_offset(math.radians(self.tilt + self.TILT_CORRECTION), self.VELOCITY)
        self.x += self.radians_x
        self.y -= self.radians_y

    def rad_to_offset(self, radians, offset):
        x = math.cos(radians) * offset
        y = math.sin(radians) * offset
        self.radians_x = x
        self.radians_y = y
    
    def detect_border(self):
        if self.x <= -25:
            self.x = 1025
        elif self.x >= 1025:
            self.x = -25
        elif self.y <= -25:
            self.y = 1025
        elif self.y >= 1025:
            self.y = -25

    def remove_bullet(self):
        if self.tick_count <= self.remove_cooldown:
            self.tick_count += 1
        else:
            self.bullets.pop(0)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
              
class Asteroid:
    TILT_CORRECTION = 90
    def __init__(self, x, y, direction, size):
        self.x = x
        self.y = y
        self.direction = direction
        self.radians_x = 0
        self.radians_y = 0
        self.img = random.choice(ASTEROID_IMGS)
        self.size = size
        self.velocity = 0
        self.size_changes()


    def draw(self):
        WIN.blit(self.img, (self.x, self.y))
        self.glide()
        self.detect_border()  

    def size_changes(self):
        if self.size == 3:
            self.velocity = 1.5
        if self.size == 2:
            self.velocity = 2.5
            self.img = pygame.transform.scale(self.img, (int(ASTEROIDWIDTH/1.5), int(ASTEROIDHEIGHT/1.5)))
        if self.size == 1:
            self.velocity = 3 
            self.img = pygame.transform.scale(self.img, (ASTEROIDWIDTH//2, ASTEROIDHEIGHT//2))

# CURRENTLY WORKING ON ASTEROIDS SPLITTING
    def split(self, asteroids):
        self.size -= 1
        for asteroid in range(0, 2):
            if self.size == 0:
                pass
            else:
                turn_direction = random.randint(self.direction - 90, self.direction + 90)
                asteroids.append(Asteroid(self.x, self.y, turn_direction, self.size))

    def detect_border(self):
        if self.x <= -25:
            self.x = 1025
        elif self.x >= 1025:
            self.x = -25
        elif self.y <= -25:
            self.y = 1025
        elif self.y >= 1025:
            self.y = -25

    def glide(self):
        self.rad_to_offset(math.radians(self.direction + self.TILT_CORRECTION), self.velocity)
        self.x += self.radians_x
        self.y -= self.radians_y

    def rad_to_offset(self, radians, offset):
        x = math.cos(radians) * offset
        y = math.sin(radians) * offset
        self.radians_x = x
        self.radians_y = y
 
    def detect_collision_ship(self, ship):
        
        ship_mask = ship.get_mask()
        asteroid_mask = pygame.mask.from_surface(self.img)

        offset = (int(self.x) - int(ship.x), int(self.y) - int(ship.y))

        hit = ship_mask.overlap(asteroid_mask, offset)

        if hit:
            return True

    def detect_collision_bullet(self, bullets):
        asteroid_mask = pygame.mask.from_surface(self.img)

        for x, bullet in enumerate(bullets):
            bullet_mask = pygame.mask.from_surface(bullet.img)

            offset = (int(self.x) - int(bullet.x), int(self.y) - int(bullet.y))

            hit = bullet_mask.overlap(asteroid_mask, offset)

            if hit:
                bullets.pop(x)
                return True
        
def draw_window(WIN, ship, bullet, asteroid):
    WIN.fill(BLACK)
    if len(bullet) >= 1:
        for bullets in bullet:
            bullets.draw()
    elif len(bullet) <= 0:
        pass
    if len(asteroid) >= 1:
        for asteroids in asteroid:
            asteroids.draw()
    elif len(asteroid) <= 0:
        pass

    ship.draw()
    pygame.display.update()


def main():
    asteroid_add = 5
    bullets = []
    asteroids = []
    ship = Ship(500, 500)
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)

        for x, asteroid in enumerate(asteroids):
            if asteroid.detect_collision_ship(ship):
                run = False
            if asteroid.detect_collision_bullet(bullets):
                asteroid.split(asteroids)
                asteroids.pop(x)


        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < 4:
                    bullets.append(Bullet(ship, bullets))
        
        if len(asteroids) <= 0:
            for add in range(0, asteroid_add):
                x = random.randint(0, 1000)
                y = random.randint(0, 1000)
                direction = random.randint(0, 360)
                if x >= ship.x - 100 and x <= ship.x + 100 and y >= ship.y - 100 and y <= ship.y + 100:
                    pass 
                else:
                    asteroids.append(Asteroid(x, y, direction, 3))
            asteroid_add += 1

        keys_pressed = pygame.key.get_pressed()
        ship.ship_movement(keys_pressed)
        draw_window(WIN, ship, bullets, asteroids)

    pygame.quit()

main()