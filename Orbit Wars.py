# Import function libraries
import pygame
import math

# victory
win = 0
# fuel
deltav1 = 50
deltav2 = 50
# Speed in pixels per frame
x_speed1 = 0
y_speed1 = 0
x_speed2 = 0
y_speed2 = 0
xgrav1 = 0.0
ygrav1 = 0.0
xgrav2 = 0.0
ygrav2 = 0.0
# Current position
x_coord1 = 100
y_coord1 = 125
x_coord2 = 1100
y_coord2 = 825
# shooty
crash1 = False
crash2 = False
# planet
centerx = 600
centery = 475
# mun
moonx = 0
moony = 0
moondegree = 0
# depots
fuelx1 = 0
fuely1 = 0
fueldegree1 = 0
fuelx2 = 0
fuely2 = 0
fueldegree2 = 1440

rocket_list = pygame.sprite.Group()
dead_list = pygame.sprite.Group()
class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pygame.Surface([4, 4])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.track = ""
        self.speedx = 0
        self.speedy = 0
        self.owner = 0
        self.timer = -1
        self.gravx = 0.0
        self.gravy = 0.0
        self.emp = False
 
    def update(self):

        if self.speedy > 25:
            self.speedy = 25
        elif self.speedy < -25:
            self.speedy = -25
        if self.speedx > 25:
            self.speedx = 25
        elif self.speedx < -25:
            self.speedx = -25
        
        self.rect.x += self.speedx * 2
        self.rect.y += self.speedy * 2
        
        self.rect.x += self.gravx
        self.rect.y += self.gravy
        self.gravx = 0.0
        self.gravy = 0.0
        
        if self.rect.x >= 1200:
            self.rect.x = 0
        elif self.rect.x <= 0:
            self.rect.x = 1200
        elif self.rect.y >= 925:
            self.rect.y = 25
        elif self.rect.y <= 25:
            self.rect.y = 925

#Are you ready for some literal rocket science?
#==============================================
#The gravitational constant in this universe in pixels^3 kg^-1 s^-2. The real one is 6.67384*(10^-11) m^3 kg^-1 s^-2
G = 2000.0
#Masses for various objects (moon, planet, and depots are not subject to gravity. Just ships and rockets)
shipmass = 0.1
missilemass = 0.1
planetmass = 50.0
moonmass = 1.0
def add_forces():
    global x_coord1
    global y_coord1
    global x_coord2
    global y_coord2
    global xgrav1
    global ygrav1
    global xgrav2
    global ygrav2
    global crash1
    global crash2
    global moonx
    global moony
    global centerx
    global centery
    global rocket_list
    global dead_list
    
    # Player 1
    # Planet
    dx = centerx - x_coord1
    dy = centery - y_coord1
    if dx > -65 and dx < 65 and dy > -65 and dy < 65:
        crash1 = True
    else:
        r_squared = dx*dx + dy*dy
        r = r_squared**0.5
        # Gravity * ship mass * planet mass / distance
        force_magnitude = (G * shipmass * planetmass) / r_squared
        dx_normalized_scaled = (dx / r) * force_magnitude
        dy_normalized_scaled = (dy / r) * force_magnitude
        xgrav1 += dx_normalized_scaled
        ygrav1 += dy_normalized_scaled
    # Moon
    dx = moonx - x_coord1
    dy = moony - y_coord1
    if dx < 10 and dx > -10 and dy < 10 and dy > -10:
        crash1 = True
    else:
        r_squared = dx*dx + dy*dy
        r = r_squared**0.5
        # Gravity * ship mass * moon mass / distance
        force_magnitude = (G * shipmass * moonmass) / r_squared
        dx_normalized_scaled = (dx / r) * force_magnitude
        dy_normalized_scaled = (dy / r) * force_magnitude
        xgrav1 += dx_normalized_scaled
        ygrav1 += dy_normalized_scaled

    # Player 2
    # Planet
    dx = centerx - x_coord2
    dy = centery - y_coord2
    if dx > -65 and dx < 65 and dy > -65 and dy < 65:
        crash2 = True
    else:
        r_squared = dx*dx + dy*dy
        r = r_squared**0.5
        # Gravity * ship mass * planet mass / distance = total force
        force_magnitude = (G * shipmass * planetmass) / r_squared
        dx_normalized_scaled = (dx / r) * force_magnitude
        dy_normalized_scaled = (dy / r) * force_magnitude
        xgrav2 += dx_normalized_scaled
        ygrav2 += dy_normalized_scaled
    # Moon
    dx = moonx - x_coord2
    dy = moony - y_coord2
    if dx < 10 and dx > -10 and dy < 10 and dy > -10:
        crash2 = True
    else:
        r_squared = dx*dx + dy*dy
        r = r_squared**0.5
        # Gravity * ship mass * moon mass / distance = total force
        force_magnitude = (G * shipmass * moonmass) / r_squared
        dx_normalized_scaled = (dx / r) * force_magnitude
        dy_normalized_scaled = (dy / r) * force_magnitude
        xgrav2 += dx_normalized_scaled
        ygrav2 += dy_normalized_scaled

    # Missiles
    for rocket in rocket_list:
        # Planet
        dx = centerx - rocket.rect.x
        dy = centery - rocket.rect.y
        if dx < 65 and dx > -65 and dy < 65 and dy > -65:
            rocket_list.remove(rocket)
            dead_list.add(rocket)
            rocket.timer = 20
        else:
            r_squared = dx*dx + dy*dy
            r = r_squared**0.5
            # Gravity * missile mass * planet mass / distance = total force
            force_magnitude = (G * missilemass * planetmass) / r_squared
            dx_normalized_scaled = (dx / r) * force_magnitude
            dy_normalized_scaled = (dy / r) * force_magnitude
            #rocket.gravx += dx_normalized_scaled
            #rocket.gravy += dy_normalized_scaled
            
        # Moon
        dx = moonx - rocket.rect.x
        dy = moony - rocket.rect.y
        if dx < 7 and dx > -7 and dy < 7 and dy > -7:
            rocket_list.remove(rocket)
            dead_list.add(rocket)
            rocket.timer = 20
        else:
            r_squared = dx*dx + dy*dy
            r = r_squared**0.5
            # Gravity * missile mass * moon mass / distance = total force
            force_magnitude = (G * missilemass * moonmass) / r_squared
            dx_normalized_scaled = (dx / r) * force_magnitude
            dy_normalized_scaled = (dy / r) * force_magnitude
            #rocket.gravx += dx_normalized_scaled
            #rocket.gravy += dy_normalized_scaled
    
def circular_orbit(centerx, centery, radius, speed, time):
    theta = math.fmod(time * speed, math.pi * 2)
    c = math.cos(theta)
    s = math.sin(theta)
    return centerx + radius * c, centery + radius * s
#==============================================

def refuel():
    global deltav1
    global deltav2
    
    # Player 1
    dx = fuelx1 - x_coord1
    dy = fuely1 - y_coord1
    if dx > -25 and dx < 25 and dy > -25 and dy < 25 and deltav1 < 999 and crash1 == False:
        deltav1 += 1
    dx = fuelx2 - x_coord1
    dy = fuely2 - y_coord1
    if dx > -25 and dx < 25 and dy > -25 and dy < 25 and deltav1 < 999 and crash1 == False:
        deltav1 += 1
    
    # Player 2
    dx = fuelx1 - x_coord2
    dy = fuely1 - y_coord2
    if dx > -25 and dx < 25 and dy > -25 and dy < 25 and deltav2 < 999 and crash2 == False:
        deltav2 += 1
    dx = fuelx2 - x_coord2
    dy = fuely2 - y_coord2
    if dx > -25 and dx < 25 and dy > -25 and dy < 25 and deltav2 < 999 and crash2 == False:
        deltav2 += 1

def draw_ship(screen, size, colour, x, y):
    pygame.draw.rect(screen, colour, [x - (size / 2), y - (size / 2), size, size], 0)

def draw_planet(screen, size, colour, x, y):
    pygame.draw.circle(screen, colour, [x, y], size, 0)

def draw_bar(screen):
    pygame.draw.rect(screen, WHITE, [0, 0, 1200, 25], 0)
    
    font = pygame.font.SysFont('Calibri', 25, True, False)
    # Player 1 readouts
    if deltav1 < 20:
        text = font.render("DeltaV: "+str(deltav1), True, RED)
    else:
        text = font.render("DeltaV: "+str(deltav1), True, BLACK)
    screen.blit(text, [10, 0])
    text = font.render("HV: "+str(x_speed1), True, BLACK)
    screen.blit(text, [140, 0])
    text = font.render("VV: "+str(y_speed1), True, BLACK)
    screen.blit(text, [220, 0])
    # Player 2 readouts
    if deltav2 < 20:
        text = font.render("DeltaV: "+str(deltav2), True, RED)
    else:
        text = font.render("DeltaV: "+str(deltav2), True, BLACK)
    screen.blit(text, [910, 0])
    text = font.render("HV: "+str(x_speed2), True, BLACK)
    screen.blit(text, [1040, 0])
    text = font.render("VV: "+str(y_speed2), True, BLACK)
    screen.blit(text, [1120, 0])

def draw_victory(screen, player):
    #pygame.draw.rect(screen, WHITE, [0, 0, 1200, 925], 0)

    if player == 1:
        colour = BLUE
    if player == 2:
        colour = RED
    
    font = pygame.font.SysFont('Calibri', 100, True, False)
    text = font.render("PLAYER "+str(player)+" WINS", True, colour)
    screen.blit(text, [300, 425])
    
# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (125, 125, 125)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (165, 165, 0)
WARN = (55, 0, 0)

PI = 3.141592653

# Set the height and width of the screen
size = (1200, 925)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Orbit Wars")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

# Loop as long as done == False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # User pressed down on a key
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and deltav1 > 0 and x_speed1 > -99 and crash1 == False:
                x_speed1 += -1
                deltav1 += -1
                track1 = "LEFT"
            elif event.key == pygame.K_d and deltav1 > 0 and x_speed1 < 99 and crash1 == False:
                x_speed1 += 1
                deltav1 += -1
                track1 = "RIGHT"
            elif event.key == pygame.K_w and deltav1 > 0 and y_speed1 < 99 and crash1 == False:
                y_speed1 += -1
                deltav1 += -1
                track1 = "UP"
            elif event.key == pygame.K_s and deltav1 > 0 and y_speed1 > -99 and crash1 == False:
                y_speed1 += 1
                deltav1 += -1
                track1 = "DOWN"

            if event.key == pygame.K_LSHIFT and crash1 == False and deltav1 > 9:
                rocket1 = Rocket()
                deltav1 += -10
                # Set the bullet so it is where the player is
                rocket1.rect.x = x_coord1
                rocket1.rect.y = y_coord1
                rocket1.owner = 1
                # Set rocket direction
                #rocket1.track = track1
                rocket1.speedx = x_speed1
                rocket1.speedy = y_speed1
                # Add the bullet to the lists
                rocket1.emp = False
                rocket_list.add(rocket1)
            elif event.key == pygame.K_LCTRL and crash1 == False and deltav1 > 9:
                rocket1 = Rocket()
                deltav1 += -10
                # Set the bullet so it is where the player is
                rocket1.rect.x = x_coord1
                rocket1.rect.y = y_coord1
                rocket1.owner = 1
                # Set rocket direction
                #rocket1.track = track1
                rocket1.speedx = x_speed1
                rocket1.speedy = y_speed1
                # Add the bullet to the lists
                rocket1.emp = True
                rocket_list.add(rocket1)
                
            if event.key == pygame.K_LEFT and deltav2 > 0 and x_speed2 > -99 and crash2 == False:
                x_speed2 += -1
                deltav2 += -1
                track2 = "LEFT"
            elif event.key == pygame.K_RIGHT and deltav2 > 0 and x_speed2 < 99 and crash2 == False:
                x_speed2 += 1
                deltav2 += -1
                track2 = "RIGHT"
            elif event.key == pygame.K_UP and deltav2 > 0 and y_speed2 < 99 and crash2 == False:
                y_speed2 += -1
                deltav2 += -1
                track2 = "UP"
            elif event.key == pygame.K_DOWN and deltav2 > 0 and y_speed2 > -99 and crash2 == False:
                y_speed2 += 1
                deltav2 += -1
                track2 = "DOWN"
                
            if event.key == pygame.K_RSHIFT and crash2 == False and deltav2 > 9:
                rocket2 = Rocket()
                deltav2 += -10
                # Set the bullet so it is where the player is
                rocket2.rect.x = x_coord2
                rocket2.rect.y = y_coord2
                rocket2.owner = 2
                # Set rocket direction
                #rocket2.track = track2
                rocket2.speedx = x_speed2
                rocket2.speedy = y_speed2
                # Add the bullet to the lists
                rocket2.emp = False
                rocket_list.add(rocket2)
            elif event.key == pygame.K_RCTRL and crash2 == False and deltav1 > 9:
                rocket2 = Rocket()
                deltav2 += -10
                # Set the bullet so it is where the player is
                rocket2.rect.x = x_coord2
                rocket2.rect.y = y_coord2
                rocket2.owner = 2
                # Set rocket direction
                #rocket2.track = track2
                rocket2.speedx = x_speed2
                rocket2.speedy = y_speed2
                # Add the bullet to the lists
                rocket2.emp = True
                rocket_list.add(rocket2)
                
    # All drawing code happens after the for loop and but
    # inside the main while not done loop.

    if x_coord1 >= 1200:
        x_coord1 = 0
    elif x_coord1 <= 0:
        x_coord1 = 1200
    elif y_coord1 >= 925:
        y_coord1 = 25
    elif y_coord1 <= 25:
        y_coord1 = 925

    if y_speed1 > 5:
        y_speed1 = 5
    elif y_speed1 < -5:
        y_speed1 = -5
    if x_speed1 > 5:
        x_speed1 = 5
    elif x_speed1 < -5:
        x_speed1 = -5

    if x_coord2 >= 1200:
        x_coord2 = 0
    elif x_coord2 <= 0:
        x_coord2 = 1200
    elif y_coord2 >= 925:
        y_coord2 = 25
    elif y_coord2 <= 25:
        y_coord2 = 925

    if y_speed2 > 5:
        y_speed2 = 5
    elif y_speed2 < -5:
        y_speed2 = -5
    if x_speed2 > 5:
        x_speed2 = 5
    elif x_speed2 < -5:
        x_speed2 = -5
    
    refuel()

    # Move the object according to the speed vector.
    x_coord1 += x_speed1
    y_coord1 += y_speed1
    x_coord2 += x_speed2
    y_coord2 += y_speed2
    
    x_coord1 += xgrav1
    y_coord1 += ygrav1
    x_coord2 += xgrav2
    y_coord2 += ygrav2
    
    xgrav1 = 0.0
    ygrav1 = 0.0
    xgrav2 = 0.0
    ygrav2 = 0.0
    
    # Clear the screen and set the screen background
    screen.fill(BLACK)

    # Execute rocket science (orbits and gravity)
    RadiusMoon = 250
    RadiusDepot1 = 50
    RadiusDepot2 = 400
    
    if moondegree < 1440:
        moondegree += 1
    else:
        moondegree = 1
        
    if fueldegree1 < 720:
        fueldegree1 += 1
    else:
        fueldegree1 = 1
    if fueldegree2 < 2880:
        fueldegree2 += 1
    else:
        fueldegree2 = 1
        
    moonx = int(math.cos((moondegree / 2) * math.pi / 360) * RadiusMoon) + centerx
    moony = int(math.sin((moondegree / 2) * math.pi / 360) * RadiusMoon) + centery
    fuelx1 = int(math.cos(fueldegree1 * math.pi / 360) * RadiusDepot1) + moonx
    fuely1 = int(math.sin(fueldegree1 * math.pi / 360) * RadiusDepot1) + moony
    fuelx2 = int(math.cos((fueldegree2 / 4) * math.pi / 360) * RadiusDepot2) + centerx
    fuely2 = int(math.sin((fueldegree2 / 4) * math.pi / 360) * RadiusDepot2) + centery

    add_forces()

    # Draw the gravity wells
    draw_planet(screen, 150, WARN, centerx, centery)
    draw_planet(screen, 25, WARN, moonx, moony)

    # Players
    if crash1 == False:
        draw_ship(screen, 10, BLUE, x_coord1, y_coord1)
    else:
        for rocket in rocket_list:
            if rocket.owner == 1:
                rocket_list.remove(rocket)
                dead_list.add(rocket)
                rocket.timer = 20
    if crash2 == False:
        draw_ship(screen, 10, RED, x_coord2, y_coord2)
    else:
        for rocket in rocket_list:
            if rocket.owner == 2:
                rocket_list.remove(rocket)
                dead_list.add(rocket)
                rocket.timer = 20

    # Calculate missles
    rocket_list.update()
    rocket_list.draw(screen)
    
    for missile in rocket_list:
        if missile.emp == False:
            detonation = 40
        if missile.emp == True:
            detonation = 70
        dx = math.fabs(x_coord2 - missile.rect.x)
        dy = math.fabs(y_coord2 - missile.rect.y)
        if missile.owner == 1:
            if dx < detonation and dy < detonation:
                rocket_list.remove(missile)
                dead_list.add(missile)
                missile.timer = 20
            
        dx = math.fabs(x_coord1 - missile.rect.x)
        dy = math.fabs(y_coord1 - missile.rect.y)
        if missile.owner == 2:
            if dx < detonation and dy < detonation:
                rocket_list.remove(missile)
                dead_list.add(missile)
                missile.timer = 20

        for torpedo in rocket_list:
            dx = math.fabs(torpedo.rect.x - missile.rect.x)
            dy = math.fabs(torpedo.rect.y - missile.rect.y)
            if dx != 0 and dy != 0:
                if torpedo.owner != missile.owner:
                    if dx < detonation and dy < detonation:
                        rocket_list.remove(missile)
                        dead_list.add(missile)
                        missile.timer = 20
                        

    for rocket in dead_list:

        if rocket.timer <= 0:
            radius = -1
            dead_list.remove(rocket)
            
        if rocket.emp == False:
            time = int(math.fabs(rocket.timer - 20))
            radius = int(time*3)

            R = int(255)
            G = int(250 - (time*10))
            B = int(255 - (time*15))
            if B < 0:
                B = 0
            elif B < 60:
                B += 5
            
            draw_planet(screen, radius, (R,G,B), rocket.rect.x, rocket.rect.y)

            # Player 1 collision
            dx = math.fabs(rocket.rect.x - x_coord1)
            dy = math.fabs(rocket.rect.y - y_coord1)
            if dx < radius and dy < radius and crash1 == False:
                crash1 = True
    
            # Player 2 collision
            dx = math.fabs(rocket.rect.x - x_coord2)
            dy = math.fabs(rocket.rect.y - y_coord2)
            if dx < radius and dy < radius and crash2 == False:
                crash2 = True

            # Other missiles collision
            for torpedo in rocket_list:
                dx = math.fabs(rocket.rect.x - torpedo.rect.x)
                dy = math.fabs(rocket.rect.y - torpedo.rect.y)
                if dx < radius and dy < radius:
                    rocket_list.remove(torpedo)
                    dead_list.add(torpedo)
                    torpedo.timer = 20

        elif rocket.emp == True:
            time = int(math.fabs(rocket.timer - 20))
            radius = int(time*5)

            R = int(255 - (time*15))
            G = int(250 - (time*10))
            B = int(255)
            if R < 0:
                R = 0
            elif R < 60:
                R += 5
            
            draw_planet(screen, radius, (R,G,B), rocket.rect.x, rocket.rect.y)

            # Player 1 collision
            dx = math.fabs(rocket.rect.x - x_coord1)
            dy = math.fabs(rocket.rect.y - y_coord1)
            if dx < radius and dy < radius and crash1 == False:
                x_speed1 = 0
                y_speed1 = 0
    
            # Player 2 collision
            dx = math.fabs(rocket.rect.x - x_coord2)
            dy = math.fabs(rocket.rect.y - y_coord2)
            if dx < radius and dy < radius and crash2 == False:
                x_speed2 = 0
                y_speed2 = 0

            # Other missiles collision
            for torpedo in rocket_list:
                dx = math.fabs(rocket.rect.x - torpedo.rect.x)
                dy = math.fabs(rocket.rect.y - torpedo.rect.y)
                if dx < radius and dy < radius:
                    rocket_list.remove(torpedo)
                    dead_list.add(torpedo)
                    torpedo.timer = 20
            
        rocket.timer -= 1

    # Planets and moons
    pygame.draw.ellipse(screen, WHITE, [centerx-RadiusMoon, centery-RadiusMoon, RadiusMoon*2, RadiusMoon*2], 1)
    draw_planet(screen, 10, GREY, moonx, moony)
    pygame.draw.ellipse(screen, WHITE, [moonx-RadiusDepot1, moony-RadiusDepot1, RadiusDepot1*2, RadiusDepot1*2], 1)
    draw_ship(screen, 10, YELLOW, fuelx1, fuely1)
    pygame.draw.ellipse(screen, WHITE, [centerx-RadiusDepot2, centery-RadiusDepot2, RadiusDepot2*2, RadiusDepot2*2], 1)
    draw_ship(screen, 10, YELLOW, fuelx2, fuely2)
    
    draw_planet(screen, 75, GREEN, centerx, centery)
    
    draw_bar(screen)

    if crash2 == True and crash1 == False and win == 0:
        win = 1
    if crash1 == True and crash2 == False and win == 0:
        win = 2

    if win != 0:
        draw_victory(screen, win)

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()
 
    # This limits the while loop to a max of 60 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(60)
 
# Be IDLE friendly
pygame.quit()
