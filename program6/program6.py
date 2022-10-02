"""
Author: Jeremy Castagno
Description: Create a Ball Catching Game
"""

import math
import random

import utime
import machine
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER
from pimoroni import Buzzer, Button

# configurable parameters
cup_width = 30 # how wide is the cup, wider make it easier
ball_radius = 10 # radius of each ball, bigger makes it easier
balls_per_second = 1 # how many balls appear per second
ball_speed = 5 # how fast does a ball fall per second
ball_color = (0, 255, 0)
cup_speed = 5 # pixels/frame
cup_height = 20 # how tall the cup is in pixels
cup_color = (255, 0 , 0)
game_loop_sleep = 30 # ms

ms_per_ball = int(1 / (balls_per_second / 1000))

# setup the display
display = PicoGraphics(display=DISPLAY_PICO_EXPLORER)
# get width and height of display
WIDTH, HEIGHT = display.get_bounds()
# get background color pen (dark grey)
BG = display.create_pen(40, 40, 40)
CP = display.create_pen(*cup_color)
BC = display.create_pen(*ball_color)
WHITE = display.create_pen(255, 255, 255)

# Create a buzzer on pin 0
# Don't forget to wire GP0 to AUDIO!
buzzer = Buzzer(0)

# create our buttons for input
button_a = Button(12, repeat_time=30, hold_time=10000)
button_b = Button(13, repeat_time=30, hold_time=10000)
button_x = Button(14, repeat_time=30, hold_time=10000)
button_y = Button(15, repeat_time=30, hold_time=10000)


def process_input(game_state):
    game_state['a_pressed'] = button_a.read()
    game_state['x_pressed'] = button_x.read()
    game_state['b_pressed'] = button_b.read()
    game_state['y_pressed'] = button_y.read()

    return game_state

def create_ball():
    radius = ball_radius
    x_pos = random.randint(radius, radius + (WIDTH - 2 * radius))
    y_pos = 0
    color = (0, 255, 0)
    return dict(radius=radius, x_pos=x_pos, y_pos=y_pos, color=color, collision=False)


def process_ball_locations(gs):
    # process ball locations
    for ball in gs['ball_list']:
        ball['y_pos'] += ball_speed


# Check collision
def check_circle_rect_collision(cx, cy, radius, rx, ry, rw, rh):
    """Check for a collision between a circle and rectangle

    Args:
        cx (float): x center of circle
        cy (float): y center of circle
        radius (float): radius of circle
        rx (float): top left x of rectangle
        ry (float): top left y of rectangle
        rw (float): width of rectangle
        rh (float): height of rectangle

    Returns:
        bool: True if there is a collision
    """
    # temporary variables to set edges for testing
    testX = cx
    testY = cy

    # which edge is closest?
    if cx < rx:
        testX = rx      # test left edge
    elif cx > (rx+rw): 
        testX = rx+rw   # right edge

    if cy < ry:         
        testY = ry      # top edge
    elif cy > ry+rh:
        testY = ry+rh   # bottom edge

    # get distance from closest edges
    distX = cx-testX
    distY = cy-testY
    distance = math.sqrt( (distX*distX) + (distY*distY) )

    # if the distance is less than the radius, collision!
    return distance <= radius


def process_game_logic(gs):
    now = utime.ticks_ms()

    # create a new ball if required
    if abs(now - gs['utime_ball']) > ms_per_ball:
        gs['utime_ball'] = now
        gs['ball_list'].append(create_ball())

    # process ball locations
    for ball in gs['ball_list']:
        ball['y_pos'] += ball_speed

    # process cup location
    if gs['a_pressed']:
        pass
    if gs['x_pressed']:
        pass    
    if gs['b_pressed']:
        gs['cup_x'] -= cup_speed
    if gs['y_pressed']:
        gs['cup_x'] += cup_speed
    gs['cup_x'] = min(WIDTH-cup_width, gs['cup_x'])
    gs['cup_x'] = max(0, gs['cup_x'])

    # check for collision
    # process ball locations
    for ball in gs['ball_list']:
        ball_x = ball['x_pos']
        ball_y = ball['y_pos']
        ball_radius = ball['radius']
        # print(ball_x, ball_y, ball_radius)
        collision = check_circle_rect_collision(ball_x, ball_y, ball_radius, gs['cup_x'], gs['cup_y'], cup_width, cup_height)
        if collision:
            print("Score!")
            gs['score'] += 1
            ball['collision'] = True

    # remove collision
    gs['ball_list'] = [ball for ball in gs['ball_list'] if not ball['collision'] and ball['y_pos'] < HEIGHT - 2]
    gs['frame_count'] += 1
    return gs


def draw_game_state(game_state):
    # Clear the screen
    display.set_pen(BG)
    display.clear()

    # Draw the cup
    display.set_pen(CP)
    display.rectangle(game_state['cup_x'], game_state['cup_y'] , cup_width, cup_height)

    # Draw the balls
    display.set_pen(BC)
    for ball in game_state['ball_list']:
        ball_x = ball['x_pos']
        ball_y = ball['y_pos']
        ball_radius = ball['radius']
        display.circle(int(ball_x), int(ball_y), int(ball_radius))

    # draw the score
    display.set_pen(WHITE)                            # change the pen colour
    display.text(f"SCORE: {game_state['score']:03}", 10, 0, 250, 4)
    display.update()

    return game_state


game_state = dict(
    a_pressed=False,
    x_pressed=False,
    b_pressed=False,
    y_pressed=False,
    cup_x=int(WIDTH/2.0), # x pos of cup
    cup_y=HEIGHT-cup_height, # y pos of cup
    utime_ball=utime.ticks_ms(), # last time a ball was created
    ball_list=[], # list of all the balls on the screen
    frame_count=0, # current frame count
    score=0 # current score
)


# game loop!
while True:
    game_state = process_input(game_state)

    game_state = process_game_logic(game_state)

    game_state = draw_game_state(game_state)

    utime.sleep_ms(game_loop_sleep)



