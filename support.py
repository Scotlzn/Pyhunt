import pygame, json, math
from random import randint
from os import walk
from settings import *

def save_json(path, data):
    j = json.dumps(data)
    with open(path+'.json', 'w') as f:
        f.write(j)
        f.close()

def load_json(path):
    d = json.load(open(path+'.json'))
    return d

def get_random_colour():
    return tuple([randint(1, 254), randint(1, 254), randint(1, 254)])

def fix_mouse(mouse_input):
    UPSCALE = WINDOW_SIZE[0] / DISPLAY_SIZE[0]
    out = []
    out.append(math.floor(mouse_input[0] / UPSCALE))
    out.append(math.floor(mouse_input[1] / UPSCALE))
    return out

def get_shop_button_pressed(mouse_position, scroll):
    # True_y is the mouse_position y in the shop and not on the screen
    # button area set number of pixels(decimals) and the button(int) of the current button and the space in front
    # area percentage is the rounded down to the integer (this variable is the button clicked)
    # position in area is the number of pixels in the current button and just below (it resets on every 96 pixels)
    # checks to see if the number of pixels is in the button height and not just below
    # checks the x direction to see if cursor is inside the button
    origin, distance_between_buttons, button_height, shop_width = 8, 96, 84, 100
    true_y = mouse_position[1] + scroll
    button_area = (true_y - origin) / distance_between_buttons
    area_percentage = int(math.floor(button_area))
    position_in_area = round(distance_between_buttons * (button_area - area_percentage))
    if position_in_area < button_height:
        if DISPLAY_SIZE[0] - shop_width + origin <= mouse_position[0] < DISPLAY_SIZE[0] - origin:
            return area_percentage
    return -1

def generate_button_images():
    out = []
    for file in walk('assets/buttons/'):
        for img in file[-1]:
            regular_img = pygame.image.load(f'assets/buttons/{img}')
            surf = pygame.transform.scale(regular_img, (84, 84))
            out.append(surf)
    return out
