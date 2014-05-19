# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]

paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2

paddle1_vel = 0
paddle2_vel = 0

paddle_size = 100
paddle_speed = 10

p1_score = 0
p2_score = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]
    
    if direction == 'RIGHT':
        ball_vel[0] += (random.randrange(120, 240) / 60.0)
        ball_vel[1] -= (random.randrange(60, 180) / 60.0)
    elif direction == 'LEFT':
        ball_vel[0] -= (random.randrange(120, 240) / 60.0)
        ball_vel[1] -= (random.randrange(60, 180) / 60.0)


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global p1_score, p2_score  # these are ints
    
    p1_score, p2_score = 0, 0
    paddle1_pos, paddle2_pos = HEIGHT/2, HEIGHT/2
    left_or_right = random.randrange(2)
    
    if left_or_right == 0:
        spawn_ball('LEFT')
    else:
        spawn_ball('RIGHT')

    
def draw(c):
    global p1_score, p2_score, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel

    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # gutter interactions
    if ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        if ball_pos[1] > paddle2_pos + paddle_size / 2 or ball_pos[1] < paddle2_pos - paddle_size / 2:
            spawn_ball('LEFT')
            p2_score += 1
        else:
            ball_vel[0] *= -1
            ball_vel[0] += ball_vel[0] * .1
            ball_vel[1] += ball_vel[1] * .1
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        if ball_pos[1] > paddle1_pos + paddle_size / 2 or ball_pos[1] < paddle1_pos - paddle_size / 2:
            spawn_ball('RIGHT')
            p1_score += 1
        else:
            ball_vel[0] *= -1
            ball_vel[0] += ball_vel[0] * .1
            ball_vel[1] += ball_vel[1] * .1

    # high/low boundary bounces
    if ball_pos[1] + BALL_RADIUS >= HEIGHT:
        ball_vel[1] *= -1
    if ball_pos[1] - BALL_RADIUS <= 0:
        ball_vel[1] *= -1
            
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 1, "Black", "Lime")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos - (paddle_size / 2) <= 0:
        paddle1_pos = paddle_size / 2
    if paddle1_pos + (paddle_size / 2) >= HEIGHT:
        paddle1_pos = HEIGHT - paddle_size / 2
    
    if paddle2_pos - (paddle_size / 2) <= 0:
        paddle2_pos = paddle_size / 2
    if paddle2_pos + (paddle_size / 2) >= HEIGHT:
        paddle2_pos = HEIGHT - paddle_size / 2
    
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    
    # draw paddles
    paddle1 = c.draw_line([0, paddle1_pos], [PAD_WIDTH + 1, paddle1_pos], paddle_size, 'Red')
    paddle2 = c.draw_line([WIDTH, paddle2_pos], [WIDTH - PAD_WIDTH - 1, paddle2_pos], paddle_size, 'Blue')
    
    # draw scores
    c.draw_text(str(p2_score), (430, 40), 50, 'Silver', 'sans-serif')
    c.draw_text(str(p1_score), (140, 40), 50, 'Silver', 'sans-serif')
    
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    # w, s paddle up
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel -= paddle_speed
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel += paddle_speed
        
    # arrows paddle up
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel -= paddle_speed
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel += paddle_speed
   
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    # w, s paddle down
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
        
    # arrows paddle down
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0

        
def reset():
    new_game()


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('RESET', reset, 60)


# start frame
new_game()
frame.start()
