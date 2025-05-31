import random
import math
import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT
from ball import Ball
from paddle import Paddle
from obstacle import Obstacle
pygame.init()

#function that tells how a ball would bounce or deflect after colliding with a rectangle
def bounce_off_obstacles_function(ball,horizontal_bounce,vertical_bounce,x,y,width,height,balldx,balldy,hit_corner,touch):

    #creates lists for every corner of the rectangle
    corner_x = [x,x+width,x,x+width]
    corner_y = [y,y+height,y+height,y]

    #sets the new direction x and y variables to the original direction in case the ball doesn't hit the rectangle
    newball_direction_x = ball.direction_x
    newball_direction_y = ball.direction_y

    #creates a local variable to contain the fact whether the ball hits the rectangle in this frame
    new_touch = False

    #checks if the ball hits one of the four corners
    for i in range(4):
        #line 25-30, Caculates the direction of ball deflection after hitting a corner. From https://gamedev.stackexchange.com/questions/10911/a-ball-hits-the-corner-where-will-it-deflect
        if math.sqrt((ball.x - corner_x[i]) ** 2 + (ball.y - corner_y[i]) ** 2) <= 5:
            xx = ball.x - corner_x[i]
            yy = ball.y - corner_y[i]
            c = -2 * (balldx * xx + balldy * yy) / (xx * xx + yy * yy)
            balldx = balldx + c * xx 
            balldy = balldy + c * yy 

            #checks if the ball was touching the rectangle in the preveious frame, prevents the ball from getting stuck into the moving rectangle or changing direction twice
            if not touch:
                newball_direction_x = ball.x + balldx
                newball_direction_y = ball.y + balldy
                hit_corner = True

            #not letting the ball bounce
            horizontal_bounce = False
            vertical_bounce = False

            #the ball collides with the rectangle
            new_touch = True

            return horizontal_bounce,vertical_bounce,newball_direction_x,newball_direction_y,hit_corner,new_touch

    #checks if the ball hits the left and right sides
    if ((ball.x + 5 >= x and ball.x + 5 <= x + width) or (ball.x - 5 <= x + width and ball.x - 5 >= x)) and ball.y >= y and ball.y <= y + height:

        #bounces the ball horizontally if the ball wasn't touching the rectangle in the preveious frame
        if not touch and horizontal_bounce:
            horizontal_bounce = False
        elif not touch and not horizontal_bounce:
            horizontal_bounce = True
        new_touch = True

    #checks if the ball hits the top and bottom sides
    elif ((ball.y + 5 >= y and ball.y + 5 <= y + height) or (ball.y - 5 <= y + height and ball.y - 5 >= y)) and ball.x >= x and ball.x <= x + width:

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

    return horizontal_bounce,vertical_bounce,newball_direction_x,newball_direction_y,hit_corner,touch


def bounce_off_bricks_function(ball,horizontal_bounce,vertical_bounce,x,y,width,height,brick):
    changes = 0
    if ((ball.x + 5 >= x and ball.x + 5 <= x + width) or (ball.x - 5 <= x + width and ball.x - 5 >= x)) and ball.y >= y and ball.y <= y + height:
        if horizontal_bounce:
            horizontal_bounce = False
        else:
            horizontal_bounce = True
        changes += 1
    if ((ball.y + 5 >= y and ball.y + 5 <= y + height) or (ball.y - 5 <= y + height and ball.y - 5 >= y)) and ball.x >= x and ball.x <= x + width:
        if vertical_bounce:
            vertical_bounce = False
        else:
            vertical_bounce = True
        changes += 1
    if changes != 0:
        brick += 1
    return horizontal_bounce,vertical_bounce,brick

def bounce_off_table_function(ball,horizontal_bounce,vertical_bounce,paddle,width,height,caught,touch):
    x = paddle.x
    y = paddle.y
    corner_x = [x,x+width,x,x+width]
    corner_y = [y,y+height,y+height,y]
    new_touch = False

    if ((ball.x + 5 >= x and ball.x + 5 <= x + width) or (ball.x - 5 <= x + width and ball.x - 5 >= x)) and ball.y >= y and ball.y <= y + height:
        if horizontal_bounce:
            horizontal_bounce = False
        else:
            horizontal_bounce = True
        new_touch = True

    elif (ball.y + 5 >= y and ball.y + 5 <= y + height and ball.x >= x and ball.x <= x + width):    
        if vertical_bounce:
            vertical_bounce = False
        else:
            vertical_bounce = True
        caught = True
        new_touch = True

    for i in range(4):
        if math.sqrt((ball.x - corner_x[i]) ** 2 + (ball.y - corner_y[i]) ** 2) <= 5:
            caught = True
            new_touch = True

    if new_touch:
        touch = True
    else:
        touch = False

    return horizontal_bounce,vertical_bounce,caught,touch

def bounce_off_screen_function(ball,horizontal_bounce,vertical_bounce,x,y,width,height,lives):
    if ball.x + 5 >= x + width or ball.x - 5 <= x:
        if horizontal_bounce:
            horizontal_bounce = False
        else:
            horizontal_bounce = True
    if ball.y - 5 <= y:
        if vertical_bounce:
            vertical_bounce = False
        else:
            vertical_bounce = True
    if ball.y + 5 >= y + height:
        lives -= 1

    return horizontal_bounce,vertical_bounce,lives


def move_function(startingpoint_x,startingpoint_y,goal_x,goal_y,speed):
    x_offset = speed * (goal_x - startingpoint_x) / math.sqrt((goal_x - startingpoint_x) ** 2 + (goal_y - startingpoint_y) ** 2)

    y_offset = math.sqrt(speed ** 2 - x_offset ** 2)
    if goal_y < startingpoint_y:
        y_offset = -y_offset 

    return x_offset,y_offset

# ---------------------------
# Initialize global variables

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
frame = 0

start_x = 210
start_y = 380

x_offset = 0
y_offset = 0.5

touch = False
caught = 0

paddle = Paddle()
ball = Ball()
horizontal_bounce = False
vertical_bounce = False
hit_corner = False

previous_lives = 3
lives = 3

touch_list = []
for i in range(10):
    touch_list.append(False)


brick_list = []
for i in range(25):
    brick_list.append(0)

obstacles = [Obstacle(35,40),Obstacle(135,40),Obstacle(235,40),Obstacle(335,40),Obstacle(35,140),Obstacle(335,140),Obstacle(35,240),Obstacle(135,240),Obstacle(235,240),Obstacle(335,240)]


screen = pygame.display.set_mode(SIZE)
pygame.mouse.set_visible(0)
clock = pygame.time.Clock()


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
            # Adjust speed if it was an arrow key
            if event.key == pygame.K_LEFT:
                paddle.speed = -2
            elif event.key == pygame.K_RIGHT:
                paddle.speed = 2

        # User let up on a key
        elif event.type == pygame.KEYUP:
            # If it is an arrow key, set speed back to zero
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                paddle.speed = 0


    # GAME STATE UPDATES
    # All game math and comparisons happen here
    if paddle.x <= 0 and paddle.speed == -2:
        paddle.speed = 0
    elif paddle.x >= 350 and paddle.speed == 2:
        paddle.speed = 0
    paddle.x += paddle.speed

    horizontal_bounce,vertical_bounce,caught,touch = bounce_off_table_function(ball,horizontal_bounce,vertical_bounce,paddle,50,10,caught,touch)

    if touch:
        ball.x += paddle.speed

    if caught: 
        start_x = 210
        start_y = 380

        ball.direction_x = random.randrange(400)
        ball.direction_y = random.randrange(360)
        caught = False

    horizontal_bounce,vertical_bounce,lives = bounce_off_screen_function(ball,horizontal_bounce,vertical_bounce,0,0,400,400,lives)

    if lives != previous_lives:
        ball.x = 210
        ball.y = 370
        start_x = 210
        start_y = 380
        ball.direction_x = random.randrange(400)
        ball.direction_y = random.randrange(360)

        if vertical_bounce:
            vertical_bounce = False

        previous_lives = lives


    # DRAWING

    screen.fill(BLACK)  # always the first drawing command

    pygame.draw.rect(screen,WHITE,[paddle.x,paddle.y,50,10])

    for i in range(len(obstacles)):
        if obstacles[i].x < 335 and obstacles[i].y == 40:
            obstacles[i].x += 0.25
            if touch_list[i]:
                ball.x += 0.25
        elif obstacles[i].x == 335 and obstacles[i].y < 240:
            obstacles[i].y += 0.25
            if touch_list[i]:
                ball.y += 0.25
        elif obstacles[i].x == 35 and obstacles[i].y > 40:
            obstacles[i].y -= 0.25
            if touch_list[i]:
                ball.y -= 0.25
        elif obstacles[i].x > 35 and obstacles[i].y == 240:
            obstacles[i].x -= 0.25
            if touch_list[i]:
                ball.x -= 0.25
        pygame.draw.rect(screen,PURPLE,[obstacles[i].x,obstacles[i].y,30,20])

        horizontal_bounce,vertical_bounce,ball.direction_x,ball.direction_y,hit_corner,touch_list[i] = bounce_off_obstacles_function(ball,horizontal_bounce,vertical_bounce,obstacles[i].x,obstacles[i].y,30,20,x_offset,y_offset,hit_corner,touch_list[i])

    
    for column in range(5):
        for row in range(5):
            if brick_list[column*5+row] != 2:  
                if brick_list[column*5+row] == 0:
                    pygame.draw.rect(screen,GREEN,[100+row*40,80+column*30,30,20])
                elif brick_list[column*5+row] == 1:
                    pygame.draw.rect(screen,RED,[100+row*40,80+column*30,30,20])
                horizontal_bounce,vertical_bounce,brick_list[column*5+row] = bounce_off_bricks_function(ball,horizontal_bounce,vertical_bounce,100+row*40,80+column*30,30,20,brick_list[column*5+row])


    if hit_corner: 
        start_x,start_y = ball.x,ball.y

    x_offset,y_offset = move_function(start_x,start_y,ball.direction_x,ball.direction_y,1.5)

    #setting the x or y speed values to negative to let the ball bounce  
    if horizontal_bounce:
        x_offset = -x_offset

    if vertical_bounce:
        y_offset = -y_offset

    hit_corner = False

    ball.x += x_offset
    ball.y += y_offset


    pygame.draw.circle(screen, AQUA, [ball.x, ball.y], 5)

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
