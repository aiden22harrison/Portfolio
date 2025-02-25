import pygame
import os
import neat
import math
import random

WIDTH, HEIGHT = (1000, 1000)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

SHIPWIDTH, SHIPHEIGHT = (30,50)
BULLETWIDTH, BULLETHEIGHT = (5,10)
ASTEROIDWIDTH, ASTEROIDHEIGHT = (75, 75)
LINEWIDTH, LINEHEIGHT = (2, 250)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

SHIP_IMG = pygame.transform.scale(pygame.image.load(r'G:\Root\Personal\Programming\Python Fun\Astroids [FNISHED]\AI Astroids\Assets\bullet.png'), (SHIPWIDTH, SHIPHEIGHT)).convert_alpha()

BULLET_IMG = pygame.transform.scale(pygame.image.load(r'G:\Root\Personal\Programming\Python Fun\Astroids [FNISHED]\AI Astroids\Assets\Ship.png'), (BULLETWIDTH, BULLETHEIGHT)).convert_alpha()

ASTEROID_IMGS = [pygame.transform.scale(pygame.image.load(r'G:\Root\Personal\Programming\Python Fun\Astroids [FNISHED]\AI Astroids\Assets\Astroid1.png'), (ASTEROIDWIDTH, ASTEROIDHEIGHT)).convert_alpha(), 
                pygame.transform.scale(pygame.image.load(r'G:\Root\Personal\Programming\Python Fun\Astroids [FNISHED]\AI Astroids\Assets\Astroid2.png'), (ASTEROIDWIDTH, ASTEROIDHEIGHT)).convert_alpha(),
                pygame.transform.scale(pygame.image.load(r'G:\Root\Personal\Programming\Python Fun\Astroids [FNISHED]\AI Astroids\Assets\Astroid3.png'), (ASTEROIDWIDTH, ASTEROIDHEIGHT)).convert_alpha()]

LINE_IMG = pygame.transform.scale(pygame.image.load(r'G:\SteamLibrary\steamapps\common\ProjectZomboid\media\ui\LootableMaps\Line.png'), (LINEWIDTH, LINEHEIGHT)).convert_alpha()

class Ship:
    ROT_VEL = 3
    TILT_CORRECTION = 90
    ACCEL = 0.15
    DEACCEL = 0.05
    VEL_CAP = 5
    def __init__(self, x, y, ship_tag):
        self.x = x
        self.y = y
        self.img = SHIP_IMG
        self.tilt = 0
        self.vel = 0.05
        self.tick_count = 1
        self.radians_x = 0
        self.radians_y = 0
        self.reset = False
        self.moving = False
        self.ship_tag = ship_tag
        self.cooldown = 100
    
    def move_foraward(self):
        if self.reset == True:
            self.reset = False
            self.vel = self.vel/self.tick_count
            self.moving == True
        self.vel += self.ACCEL
        self.rad_to_offset(math.radians(self.tilt + self.TILT_CORRECTION), self.vel)
        self.x += self.radians_x
        self.y -= self.radians_y
        if self.vel > self.VEL_CAP:
            self.vel = self.VEL_CAP
        self.tick_count = 1
    
    def handle_friction(self):
        if self.reset == False:
                self.rad_to_offset(math.radians(self.tilt + self.TILT_CORRECTION), self.vel)
                self.reset = True
        self.x += self.radians_x/self.tick_count
        self.y -= self.radians_y/self.tick_count
        self.tick_count += self.DEACCEL
        if self.vel <= 0:
            self.vel = 0
    
    def turn_left(self): 
        self.tilt += self.ROT_VEL
        if self.tilt <= 0 and self.tilt >= 360:
            self.tilt -= self.ROT_VEL
        elif self.tilt < 0:
            self.tilt = 360
        elif self.tilt > 360:
            self.tilt = 0
        self.last_turn = 0
        self.turn_tick_count = 1
    
    def turn_right(self):
        self.tilt -= self.ROT_VEL
        if self.tilt <= 0 and self.tilt >= 360:
            self.tilt -= self.ROT_VEL
        elif self.tilt < 0:
            self.tilt = 360
        elif self.tilt > 360:
            self.tilt = 0
        self.last_turn = 1
        self.turn_tick_count = 1

    def detect_border(self):
        if self.x <= 0:
            self.x = 1000
        elif self.x >= 1000:
            self.x = 0
        elif self.y <= -15:
            self.y = 1015
        elif self.y >= 1015:
            self.y = -15

    def draw(self):
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)
        WIN.blit(rotated_image, new_rect.topleft)
        self.update_cooldown()
        self.detect_border()

    def rad_to_offset(self, radians, offset):
        x = math.cos(radians) * offset
        y = math.sin(radians) * offset
        self.radians_x = x
        self.radians_y = y

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def update_cooldown(self):
        if self.cooldown < 10:
            self.cooldown += 1
        else:
            self.cooldown = 10
        

class Bullet(Ship):
    VELOCITY = 10
    TILT_CORRECTION = 90
    def __init__(self, Ship, bullets, ship_tag):
        self.x = Ship.x + SHIPWIDTH/2
        self.y = Ship.y + SHIPHEIGHT/2
        self.tilt = Ship.tilt
        self.img = BULLET_IMG
        self.radiants_x = 0
        self.radians_y = 0
        self.tick_count = 0
        self.bullets = bullets
        self.remove_cooldown = 70
        self.ship_tag = ship_tag

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
        if self.x <= -15:
            self.x = 1015
        elif self.x >= 1015:
            self.x = -15
        elif self.y <= -15:
            self.y = 1015
        elif self.y >= 1015:
            self.y = -15

    def remove_bullet(self):
        if self.tick_count <= self.remove_cooldown:
            self.tick_count += 1
        else:
            self.bullets.pop(0)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
              
class Asteroid:
    TILT_CORRECTION = 90
    def __init__(self, x, y, direction, size, ship_tag):
        self.x = x
        self.y = y
        self.direction = direction
        self.radians_x = 0
        self.radians_y = 0
        self.img = random.choice(ASTEROID_IMGS)
        self.size = size
        self.velocity = 0
        self.size_changes()
        self.ship_tag = ship_tag


    def draw(self):
        WIN.blit(self.img, (self.x, self.y))
        self.glide()
        self.detect_border()  

    def size_changes(self):
        if self.size == 3:
            self.velocity = 3
        if self.size == 2:
            self.velocity = 3.5
            self.img = pygame.transform.scale(self.img, (int(ASTEROIDWIDTH/1.5), int(ASTEROIDHEIGHT/1.5)))
        if self.size == 1:
            self.velocity = 4
            self.img = pygame.transform.scale(self.img, (ASTEROIDWIDTH//2, ASTEROIDHEIGHT//2))

    def split(self, asteroids):
        self.size -= 1
        for asteroid in range(0, 2):
            if self.size == 0:
                pass
            else:
                turn_direction = random.randint(self.direction - 45, self.direction + 45)
                asteroids.append(Asteroid(self.x, self.y, turn_direction, self.size, self.ship_tag))

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
                if self.ship_tag == bullet.ship_tag:
                    bullets.pop(x)
                    return bullet.ship_tag

        return -1
    
    def detect_parent_ship(self, ships, asteroids):
        ship_tags = []
        asteroid_tags = []
        new_asteroids = []
        for ship in ships:
            ship_tags.append(ship.ship_tag)
        for tag in ship_tags:
            for asteroid in asteroids:
                if tag == asteroid.ship_tag:
                    new_asteroids.append(asteroid)
        return new_asteroids




def draw_window(WIN, ships, bullet, asteroid):
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

    for ship in ships:  
        ship.draw()

    pygame.display.update()

def detect_asteroid(direction, asteroids, ship):

    corrections = {0: (0, 100), 45: (0, 0), 90: (-100, 0), 135: (0, 290), 180: (0, 290), 225: (-280, 280), 270: (-290, 0), 315: (-290, 0)}
    correction_X, correction_Y = corrections[direction]

    line = pygame.transform.rotate(LINE_IMG, direction)
    line_mask = pygame.mask.from_surface(line)
    WIN.blit(line, (int(ship.x + correction_X) + SHIPWIDTH//2 - 5, int(ship.y - correction_Y) + SHIPHEIGHT//2 - 5))

    for x, asteroid in enumerate(asteroids):
        if asteroid.ship_tag == ship.ship_tag:
            asteroid_mask = pygame.mask.from_surface(asteroid.img)

            offset = (int(ship.x + correction_X) + SHIPWIDTH//2 - int(asteroid.x), int(ship.y - correction_Y) + SHIPHEIGHT//2 - int(asteroid.y))

            hit = asteroid_mask.overlap(line_mask, offset)

            if hit:
                distance = math.sqrt((asteroid.x - ship.x)**2 + (asteroid.y - ship.y)**2) - 25
                return distance
    return 0

def find_missing(lst): 
    return [x for x in range(lst[0], lst[-1]+1) if x not in lst] 

def main(genomes, config):
    nets = []
    ge = []
    ships = []
    tag = 0

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        ships.append(Ship(500, 500, tag))
        g.fitness = 0
        ge.append(g)
        tag += 1
    
    tags = []
    asteroid_add = 10
    bullets = []
    asteroids = []
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(30)

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        if len(asteroids) == 0:
            for ship in ships:
                added = 0
                while added <= asteroid_add:
                    x = random.randint(0, 1000)
                    y = random.randint(0, 1000)
                    direction = random.randint(0, 360)
                    if x >= ship.x - 300 and x <= ship.x + 300 and y >= ship.y - 300 and y <= ship.y + 300:
                        pass 
                    else:
                        asteroids.append(Asteroid(x, y, direction, 3, ship.ship_tag))
                        added += 1
                else:
                    asteroid_add += 1 

        for asteroid in asteroids:
            tags.append(asteroid.ship_tag)
        missing_tag = find_missing(tags)
        if len(missing_tag) == 0:
            tags.clear()
        elif len(missing_tag) > 0:
            tags.clear()
            for missing in missing_tag:
                for add in range(0, asteroid_add):
                    x = random.randint(0, 1000)
                    y = random.randint(0, 1000)
                    direction = random.randint(0, 360)
                if x >= ship.x - 100 and x <= ship.x + 100 and y >= ship.y - 100 and y <= ship.y + 100:
                    pass
                else:
                    asteroids.append(Asteroid(x, y, direction, 3, missing))
                    asteroid_add += 1


        bullet_tags = []
        for x, ship in enumerate(ships):
            for bullet in bullets:
                bullet_tags.append(bullet.ship_tag)
            ge[x].fitness += .35

            output = nets[x].activate((detect_asteroid(0, asteroids, ship), detect_asteroid(45, asteroids, ship), detect_asteroid(90, asteroids, ship), detect_asteroid(135, asteroids, ship), detect_asteroid(180, asteroids, ship), detect_asteroid(225, asteroids, ship), detect_asteroid(270, asteroids, ship), detect_asteroid(315, asteroids, ship)))
            
            if output[0] >= 0.5:  
                ship.move_foraward()
            else:
                ship.handle_friction()
            if output[1] >= 0.5:
                ship.turn_left()
            if output[2] >= 0.5:
                ship.turn_right()
            if output[3] >= 0.5:
                if bullet_tags.count(ship.ship_tag) < 5 and ship.cooldown >= 10:
                    bullets.append(Bullet(ship, bullets, ship.ship_tag))
                    ship.cooldown = 0
                    

        asteroids_tag = []
        for asteroid in asteroids:
            for x, ship in enumerate(ships):
                if asteroid.detect_collision_ship(ship) and ship.ship_tag == asteroid.ship_tag: 
                    ships.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    new_asteroids = asteroid.detect_parent_ship(ships, asteroids)
                    asteroids = new_asteroids

        ship_tags = []
        for x, asteroid in enumerate(asteroids):
            collision = asteroid.detect_collision_bullet(bullets)
            if collision >= 0:
                asteroid.split(asteroids)
                asteroids.pop(x)
                for ship in ships:
                    if collision == ship.ship_tag:
                        try:
                            ge[collision].fitness += 3
                        except:
                            pass           

        if len(ships) == 0:
            break
        
        draw_window(WIN, ships, bullets, asteroids)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,100000)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')

    run(config_path)


