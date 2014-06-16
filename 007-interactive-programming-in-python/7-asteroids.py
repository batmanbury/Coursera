# Runs on CodeSkulptor.org
# program template for Spaceship

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 30)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
soundtrack.set_volume(1)
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [135, 45], ship_info.get_size(),
                              self.pos, ship_info.get_size(), self.angle)
        else:
            canvas.draw_image(self.image, ship_info.get_center(), ship_info.get_size(),
                              self.pos, ship_info.get_size(), self.angle)

    def update(self):
        # position update
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # angle update
        self.angle += self.angle_vel
        
        # velocity update
        global forward
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += forward[0] * 0.45
            self.vel[1] += forward[1] * 0.45
        
        # friction update
        self.vel[0] *= (1 - 0.02)
        self.vel[1] *= (1 - 0.02)
    
    def keydown(self, key):
        if key == simplegui.KEY_MAP['left']:
            self.angle_vel += -0.175
        if key == simplegui.KEY_MAP['right']:
            self.angle_vel += 0.175
        if key == simplegui.KEY_MAP['up']:
            self.thrust = True
            ship_thrust_sound.play()
        if key == simplegui.KEY_MAP['space']:
            self.shoot()
            
    def keyup(self, key):
        if key == simplegui.KEY_MAP['left']:
            self.angle_vel = 0
        if key == simplegui.KEY_MAP['right']:
            self.angle_vel = 0
        if key == simplegui.KEY_MAP['up']:
            self.thrust = False
            ship_thrust_sound.rewind()
    
    def shoot(self):
        global forward, a_missile, missile_group
        
        missile_forward = angle_to_vector(self.angle)
        
        missile_direction = [missile_forward[0] * 45 + self.pos[0],
                             missile_forward[1] * 45 + self.pos[1]]
        
        missile_vel = [self.vel[0] + missile_forward[0] * 10,
                       self.vel[1] + missile_forward[1] * 10]
        
        a_missile = Sprite(missile_direction, missile_vel, 0, 0,
                           missile_image, missile_info, missile_sound)
        
        missile_group.add(a_missile)
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = list(info.get_center())
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            self.image_center[0] += self.age * self.image_size[0]
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
            
    
    def update(self):
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # update angle
        self.angle = self.angle + self.angle_vel
        
        # increment sprite age
        self.age += 1
        if self.age >= self.lifespan:
            return True
        else:
            return False
    
    def collide(self, other_object):
        d = dist(self.pos, other_object.pos) 
        if d  < self.radius + other_object.radius:
            return True          
        else:
            return False
        

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score
    lives = 3
    score = 0
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        soundtrack.play()
        started = True

def draw(canvas):
    global time, lives, score, started, rock_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    if started:
        my_ship.draw(canvas)

    # update ship and sprites
    my_ship.update()

    # process sprite groups
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # check for collisions
    if group_collide(rock_group, my_ship):
        lives -= 1

    if lives <= 0:
        started = False
        soundtrack.rewind()
        rock_group = set([])
        my_ship.pos = [WIDTH / 2, HEIGHT / 2]
    
    # group collisions
    collisions = group_group_collide(rock_group, missile_group)
    if collisions > 0:
        score += collisions
    
    # display lives and score
    canvas.draw_text('Ships:', (10, 30), 30, 'White', 'sans-serif')
    canvas.draw_text(str(lives), (10, 60), 30, 'White', 'sans-serif')
    canvas.draw_text('Score:', (620, 30), 30, 'White', 'sans-serif')
    canvas.draw_text(str(score), (620, 60), 30, 'White', 'sans-serif')
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
            
# timer handler that spawns a rock into rock_group
def rock_spawner():
    global started, a_rock, rock_vel, rock_ang_vel
    
    rock_vel = [random.choice([1, -1]) * random.random() * 3,
                random.choice([1, -1]) * random.random() * 3]
    
    rock_ang_vel = random.choice([1, -1]) * random.random() * 2 * math.pi * 0.03
    
    a_rock = Sprite([random.randrange(800), random.randrange(600)],  #pos
                    rock_vel,                                        #vel
                    random.randrange(-3, 3),                         #ang
                    rock_ang_vel,                                    #ang_vel
                    asteroid_image,                                  #image
                    asteroid_info)                                   #info
    
    if started and len(rock_group) < 12:
        if dist(a_rock.pos, my_ship.pos) > my_ship.radius*2.5:
            rock_group.add(a_rock)

# sprite group processor
def process_sprite_group(group,canvas):
    for sprite in set(group):
        sprite.update()
        if sprite.update():
            group.remove(sprite)
        sprite.draw(canvas)

# group collision processors
def group_collide(group, other_object):
    for sprite in set(group):
        if sprite.collide(other_object):
            expl = Sprite(other_object.pos, [0, 0], 0, 0, explosion_image,
                          explosion_info, explosion_sound)
            explosion_group.add(expl)
            group.remove(sprite)
            return True

def group_group_collide(asteroids, missiles):
    hits = 0
    for rock in set(asteroids):
        if group_collide(missiles, rock):
            asteroids.discard(rock)
            hits += 1
    return hits
        

# initialize frame
frame = simplegui.create_frame("RiceRocks", WIDTH, HEIGHT)

# initialize ship and sprite groups
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], -1.5708, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click)
if lives > 0:
    frame.set_keydown_handler(my_ship.keydown)
    frame.set_keyup_handler(my_ship.keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
