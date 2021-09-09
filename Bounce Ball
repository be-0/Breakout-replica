import random
import math
import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT
pygame.init()

#function that tells how a ball would bounce or deflect after colliding with a rectangle
def bounce_off_obstacles_function(ball_x,ball_y,horizontal_bounce,vertical_bounce,x,y,width,height,balldx,balldy,hit_corner,direction_x,direction_y,touch):
    
    #creates lists for every corner of the rectangle
    corner_x = [x,x+width,x,x+width]
    corner_y = [y,y+height,y+height,y]
    
    #sets the new direction x and y variables to the original direction in case the ball doesn't hit the rectangle
    newdirection_x = direction_x
    newdirection_y = direction_y
    
    #creates a local variable to contain the fact whether the ball hits the rectangle in this frame
    new_touch = False
    
    #checks if the ball hits one of the four corners
    for i in range(4):
        #line 25-30, Caculates the direction of ball deflection after hitting a corner. From https://gamedev.stackexchange.com/questions/10911/a-ball-hits-the-corner-where-will-it-deflect
        if math.sqrt((ball_x - corner_x[i]) ** 2 + (ball_y - corner_y[i]) ** 2) <= 5:
            xx = ball_x - corner_x[i]
            yy = ball_y - corner_y[i]
            c = -2 * (balldx * xx + balldy * yy) / (xx * xx + yy * yy)
            balldx = balldx + c * xx 
            balldy = balldy + c * yy 
            
            #checks if the ball was touching the rectangle in the preveious frame, prevents the ball from getting stuck into the moving rectangle or changing direction twice
            if not touch:
                newdirection_x = ball_x + balldx
                newdirection_y = ball_y + balldy
                hit_corner = True
            
            #not letting the ball bounce
            horizontal_bounce = False
            vertical_bounce = False
            
            #the ball collides with the rectangle
            new_touch = True
            
            return horizontal_bounce,vertical_bounce,newdirection_x,newdirection_y,hit_corner,new_touch
    
    #checks if the ball hits the left and right sides
    if ((ball_x + 5 >= x and ball_x + 5 <= x + width) or (ball_x - 5 <= x + width and ball_x - 5 >= x)) and ball_y >= y and ball_y <= y + height:
        
        #bounces the ball horizontally if the ball wasn't touching the rectangle in the preveious frame
        if not touch and horizontal_bounce:
            horizontal_bounce = False
        elif not touch and not horizontal_bounce:
            horizontal_bounce = True
        new_touch = True
    
    #checks if the ball hits the top and bottom sides
    elif ((ball_y + 5 >= y and ball_y + 5 <= y + height) or (ball_y - 5 <= y + height and ball_y - 5 >= y)) and ball_x >= x and ball_x <= x + width:
        
        #bounces the ball vertically if the ball wasn't touching the rectangle in the preveious frame
        if not touch and vertical_bounce:
            vertical_bounce = False
        elif not touch and not vertical_bounce:
            vertical_bounce = True
        new_touch = True

    #updates if the ball is touching the rectangle in this frame
    if new_touch:
        touch = True
    else: 
        touch = False 

    return horizontal_bounce,vertical_bounce,newdirection_x,newdirection_y,hit_corner,touch



def bounce_off_bricks_function(ball_x,ball_y,horizontal_bounce,vertical_bounce,x,y,width,height,brick):
    changes = 0
    if ((ball_x + 5 >= x and ball_x + 5 <= x + width) or (ball_x - 5 <= x + width and ball_x - 5 >= x)) and ball_y >= y and ball_y <= y + height:
        if horizontal_bounce:
            horizontal_bounce = False
        else:
            horizontal_bounce = True
        changes += 1
    if ((ball_y + 5 >= y and ball_y + 5 <= y + height) or (ball_y - 5 <= y + height and ball_y - 5 >= y)) and ball_x >= x and ball_x <= x + width:
        if vertical_bounce:
            vertical_bounce = False
        else:
            vertical_bounce = True
        changes += 1
    if changes != 0:
        brick += 1
    return horizontal_bounce,vertical_bounce,brick

def bounce_off_table_function(ball_x,ball_y,horizontal_bounce,vertical_bounce,x,y,width,height,caught,touch):
    corner_x = [x,x+width,x,x+width]
    corner_y = [y,y+height,y+height,y]
    new_touch = False

    if ((ball_x + 5 >= x and ball_x + 5 <= x + width) or (ball_x - 5 <= x + width and ball_x - 5 >= x)) and ball_y >= y and ball_y <= y + height:
        if horizontal_bounce:
            horizontal_bounce = False
        else:
            horizontal_bounce = True
        new_touch = True
            
    elif (ball_y + 5 >= y and ball_y + 5 <= y + height and ball_x >= x and ball_x <= x + width):    
        if vertical_bounce:
            vertical_bounce = False
        else:
            vertical_bounce = True
        caught = True
        new_touch = True
    
    for i in range(4):
        if math.sqrt((ball_x - corner_x[i]) ** 2 + (ball_y - corner_y[i]) ** 2) <= 5:
            caught = True
            new_touch = True
    
    if new_touch:
        touch = True
    else:
        touch = False

    
    
    return horizontal_bounce,vertical_bounce,caught,touch

def bounce_off_screen_function(ball_x,ball_y,horizontal_bounce,vertical_bounce,x,y,width,height,lives):
    if ball_x + 5 >= x + width or ball_x - 5 <= x:
        if horizontal_bounce:
            horizontal_bounce = False
        else:
            horizontal_bounce = True
    if ball_y - 5 <= y:
        if vertical_bounce:
            vertical_bounce = False
        else:
            vertical_bounce = True
    if ball_y + 5 >= y + height:
        lives -= 1
    
    return horizontal_bounce,vertical_bounce,lives


def move_function(startingpoint_x,startingpoint_y,goal_x,goal_y,speed):
    x_offset = speed * (goal_x - startingpoint_x) / math.sqrt((goal_x - startingpoint_x) ** 2 + (goal_y - startingpoint_y) ** 2)
    
    y_offset = math.sqrt(speed ** 2 - x_offset ** 2)
    if goal_y < startingpoint_y:
        y_offset = -y_offset 
    
    return x_offset,y_offset


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
AQUA = (0,255,255)
PURPLE = (191,62,255)

WIDTH = 400
HEIGHT = 400
SIZE = (WIDTH, HEIGHT)
my_font = pygame.font.SysFont('Arial', 100)
start_x = 210
start_y = 380
player_x = 100
player_y = 100
speed = 1
frame = 0
oframe = 0
x_speed = 0
ball_x = 210
ball_y = 370
x_coord = 175
y_coord = 380

x_offset = 0
y_offset = 0.5

horizontal_bounce = False
vertical_bounce = False


touch = False
caught = 0
direction_x = random.randrange(400)
direction_y = random.randrange(380) 
hit_corner = False

previous_lives = 3
lives = 3

touch_list = []
for i in range(10):
    touch_list.append(False)


brick_list = []
for i in range(25):
    brick_list.append(0)


obstacle_x_list = [35,135,235,335,35,335,35,135,235,335]
obstacle_y_list = [40,40,40,40,140,140,240,240,240,240]


screen = pygame.display.set_mode(SIZE)
pygame.mouse.set_visible(0)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables



time_font = pygame.font.SysFont('Arial', 25)
end_font = pygame.font.SysFont('Arial', 60)
  # tuple unpacking
# ---------------------------

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
                
        elif event.type == QUIT:
            running = False     
        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            
            if event.key == pygame.K_LEFT:
                x_speed = -2
                
            elif event.key == pygame.K_RIGHT:
                x_speed = 2
                
            

            
        # User let up on a key
        elif event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_speed = 0

    
    # GAME STATE UPDATES
    # All game math and comparisons happen here
    if x_coord <= 0 and x_speed == -2:
        x_speed = 0
    elif x_coord >= 350 and x_speed == 2:
        x_speed = 0
    x_coord += x_speed
 
    horizontal_bounce,vertical_bounce,caught,touch = bounce_off_table_function(ball_x,ball_y,horizontal_bounce,vertical_bounce,x_coord,y_coord,50,10,caught,touch)
    
    if touch:
        ball_x += x_speed

    if caught: 
        start_x = 210
        start_y = 380
        
        direction_x = random.randrange(400)
        direction_y = random.randrange(360)
        caught = False
        
        
    horizontal_bounce,vertical_bounce,lives = bounce_off_screen_function(ball_x,ball_y,horizontal_bounce,vertical_bounce,0,0,400,400,lives)
    
    if lives != previous_lives:
        ball_x = 210
        ball_y = 370
        start_x = 210
        start_y = 380
        direction_x = random.randrange(400)
        direction_y = random.randrange(360)
        
        if vertical_bounce:
            vertical_bounce = False
        
        previous_lives = lives
    
   
    
 
    # DRAWING
  
  
    screen.fill(BLACK)  # always the first drawing command
    
    pygame.draw.rect(screen,WHITE,[x_coord,y_coord,50,10])
    
    
    
    
    for i in range(len(obstacle_x_list)):
        if obstacle_x_list[i] < 335 and obstacle_y_list[i] == 40:
            obstacle_x_list[i] += 0.25
            if touch_list[i]:
                ball_x += 0.25
        elif obstacle_x_list[i] == 335 and obstacle_y_list[i] < 240:
            obstacle_y_list[i] += 0.25
            if touch_list[i]:
                ball_y += 0.25
        elif obstacle_x_list[i] == 35 and obstacle_y_list[i] > 40:
            obstacle_y_list[i] -= 0.25
            if touch_list[i]:
                ball_y -= 0.25
        elif obstacle_x_list[i] > 35 and obstacle_y_list[i] == 240:
            obstacle_x_list[i] -= 0.25
            if touch_list[i]:
                ball_x -= 0.25
        pygame.draw.rect(screen,PURPLE,[obstacle_x_list[i],obstacle_y_list[i],30,20])
        
        horizontal_bounce,vertical_bounce,direction_x,direction_y,hit_corner,touch_list[i] = bounce_off_obstacles_function(ball_x,ball_y,horizontal_bounce,vertical_bounce,obstacle_x_list[i],obstacle_y_list[i],30,20,x_offset,y_offset,hit_corner,direction_x,direction_y,touch_list[i])


    
    for column in range(5):
        for row in range(5):
            
            if brick_list[column*5+row] != 2:  
                if brick_list[column*5+row] == 0:
                    pygame.draw.rect(screen,GREEN,[100+row*40,80+column*30,30,20])
                elif brick_list[column*5+row] == 1:
                    pygame.draw.rect(screen,RED,[100+row*40,80+column*30,30,20])
                horizontal_bounce,vertical_bounce,brick_list[column*5+row] = bounce_off_bricks_function(ball_x,ball_y,horizontal_bounce,vertical_bounce,100+row*40,80+column*30,30,20,brick_list[column*5+row])
    

    if hit_corner: 
        start_x,start_y = ball_x,ball_y

    x_offset,y_offset = move_function(start_x,start_y,direction_x,direction_y,1.5)
    
    
    #setting the x or y speed values to negative to let the ball bounce  
    if horizontal_bounce:
        x_offset = -x_offset
        
    if vertical_bounce:
        y_offset = -y_offset
    
    
    
    hit_corner = False
    
    ball_x += x_offset
    ball_y += y_offset
    
  
    pygame.draw.circle(screen, AQUA, [ball_x, ball_y], 5)
       
    
    
        
    if lives > 0 and sum(brick_list) == 50:
        screen.fill((BLACK))
        text = end_font.render("You Won", True, WHITE)       
        screen.blit(text, (60, 170))
    elif lives <= 0:
        screen.fill((RED))
        text = end_font.render("Game Over", True, WHITE)       
        screen.blit(text, (60, 170))
    else:
        text = time_font.render("Lives:"+str(lives), True, WHITE)
        screen.blit(text, (160, 0))
    
   
    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(120)
    #---------------------------

pygame.quit()
