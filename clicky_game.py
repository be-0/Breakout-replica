import random
import math
import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, MOUSEBUTTONDOWN
pygame.init()

def shoot_function(startingpoint_x,startingpoint_y,goal_x,goal_y,speed):
    x_offset = speed * (goal_x - startingpoint_x) / math.sqrt((goal_x - startingpoint_x) ** 2 + (goal_y - startingpoint_y) ** 2)
    
    y_offset = math.sqrt(speed ** 2 - x_offset ** 2)
    if goal_y < startingpoint_y:
        y_offset = -y_offset 
    
    return x_offset,y_offset

def chase_function(startingpoint_x,startingpoint_y,goal_x,goal_y,speed,color):
    if goal_x - startingpoint_x != 0:
        x_offset = speed * (goal_x - startingpoint_x) / math.sqrt((goal_x - startingpoint_x) ** 2 + (goal_y - startingpoint_y) ** 2)
    
        y_offset = math.sqrt(speed ** 2 - x_offset ** 2)
        if goal_y < startingpoint_y:
            y_offset = -y_offset
    
    
        startingpoint_x += x_offset
        startingpoint_y += y_offset
        pygame.draw.circle(screen, color, [startingpoint_x, startingpoint_y], 10)
        return startingpoint_x,startingpoint_y

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (242,250,0)

WIDTH = 700
HEIGHT = 500
SIZE = (WIDTH, HEIGHT)
my_font = pygame.font.SysFont('Arial', 100)
remaining_time = 100
chaser1_x = 0
chaser1_y = 0
mouse_x = 100.01
mouse_y = 100.01
player_x = 100
player_y = 100
speed = 1
frame = 0
countdown = 11
bullet_list = []
offset = []
color = RED
explode = None
lost = None
for i in range(15):   
    offset.append([0, 0])

for n in range(5):
    for i in range(100,400,100):    
        bullet_list.append([650, i])
print(bullet_list) 
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables

score = 0

time_font = pygame.font.SysFont('Arial', 25)
end_font = pygame.font.SysFont('Arial', 60)
  # tuple unpacking
# ---------------------------

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
            print(f"x: {mouse_x}, y:{mouse_y}")
    frame += 1
    
    # GAME STATE UPDATES
    # All game math and comparisons happen here

    # DRAWING
    screen.fill((BLACK))  # always the first drawing command
    if frame % 60 == 0:
            remaining_time -= 1
        
    text = time_font.render("Survive: " + str(remaining_time), True, WHITE)
    screen.blit(text, (280, 50))
    
    player_x,player_y = chase_function(player_x, player_y, mouse_x ,mouse_y, 2, WHITE)

    

    #checks if it's time to explode every 10 seconds
    if frame % 600 == 0:             
        explode = True
        explode_x = chaser1_x
        explode_y = chaser1_y
    
    if explode:
        #draw the 'explode circle' around the bomb
        pygame.draw.circle(screen, RED, [explode_x, explode_y], 100)
        if math.sqrt((player_x - explode_x) ** 2 + (player_y - explode_y) ** 2) < 110:
            lost = True
        #after 10 sec the 'explode circle' would disappear
        if frame % 660 == 0:
            explode = False
    
    #letting the bomb respawn after the explosion
    if frame % 660 == 0:
        chaser1_x = random.randrange(0,701)
        chaser1_y = random.randrange(0,500)
        countdown = 11
    
    #checks the countdown of the bomb
    if frame % 60 == 0 and countdown > 1:      
        countdown -= 1
    
    #letting the color of bomb flash faster and faster untill it explodes 
    if frame % (countdown * 5) == 0:
            color = YELLOW
    if frame % (countdown * 5 * 2) == 0:
            color = RED
    
    
    chaser1_x,chaser1_y = chase_function(chaser1_x,chaser1_y,player_x,player_y,0.8,color)
    
    



    for i in range(len(bullet_list)):
        pygame.draw.circle(screen, YELLOW, bullet_list[i], 5)
        if math.sqrt((bullet_list[i][0] - player_x) ** 2 + (bullet_list[i][1] - player_y) ** 2) < 15:
            lost = True
            
        bullet_list[i][0] += offset[i][0]
        bullet_list[i][1] += offset[i][1]
    
    
       
        if frame % 60 == 0:
            if bullet_list[i][1] > 500 or bullet_list[i][0] < 0 or bullet_list[i][1] < 0 or bullet_list[i][0] == 650 or bullet_list[i][0] > 700:
           
                y = random.randrange(0, 8) * 100
                bullet_list[i][1] = y
 
                x = 650
                bullet_list[i][0] = x
                offset[i] = shoot_function(bullet_list[i][0],bullet_list[i][1],player_x,player_y,3)
    if lost:
        screen.fill((RED))
        text = end_font.render("You Died", True, WHITE)       
        screen.blit(text, (250, 200))
    elif remaining_time == 0:
        screen.fill((BLACK))
        text = end_font.render("You Won", True, WHITE)       
        screen.blit(text, (250, 200))
    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(60)
    #---------------------------


pygame.quit()
    


