import pygame
from support import get_random_colour, generate_button_images, load_json
from text import Text
from settings import *


class ShopManager:
    def __init__(self, ds):
        self.ds = ds

        self.x, self.y = DISPLAY_SIZE[0], 0
        self.width, self.height = 100, 360
        self.max_width = DISPLAY_SIZE[0] - 100
        self.speed = 100
        self.scroll = 0
        self.moving, self.active = False, False

        pygame.mixer.init()
        self.upgrade_sound = pygame.mixer.Sound('sounds/upgrade.wav')
        self.denied_sound = pygame.mixer.Sound('sounds/denied.wav')

        self.button_width, self.button_height = 84, 84

        self.button_images = generate_button_images()

        self.button_count = 5
        self.upgrade_data = load_json('data/shop')
        self.buttons = self.generate_buttons()

        self.button_spacing = 12
        self.distance_between_buttons = self.button_height + self.button_spacing
        # height limit is the distance between the top left of each button * the button count
        # + origin (top) - (button_spacing - origin)(bottom) the distance between last button and the bottom is 8 not 12
        self.height_limit = ((self.distance_between_buttons * self.button_count) + 8 - 4) - DISPLAY_SIZE[1]

    def generate_buttons(self):
        out = []
        for i in range(self.button_count):
            try:
                img = self.button_images[i]
            except IndexError:
                img = None
            try:
                data = self.upgrade_data[str(i)]
            except KeyError:
                data = None
            out.append(Button(self.ds, (self.button_width, self.button_height), i, img, data))
        return out

    def move(self, dt, direction):
        velocity = -self.speed if direction else self.speed
        self.x += velocity * dt
        self.moving, self.active = True, False
        if self.x < self.max_width:
            self.x = self.max_width
            self.moving, self.active = False, True
        if self.x > DISPLAY_SIZE[0]:
            self.x = DISPLAY_SIZE[0]
            self.moving = False

        if self.scroll != 0:
            if self.scroll < 0:
                self.scroll = 0
            if self.scroll > self.height_limit:
                self.scroll = self.height_limit

    def render_shop(self):
        if self.x != 640:
            pygame.draw.rect(self.ds, '#eb8034', (self.x, self.y, self.width, self.height))

    def update_buttons(self):
        for button in self.buttons:
            button.update(self.scroll, (self.x, self.y))

    def update(self, dt, active):
        self.move(dt, active)
        self.render_shop()
        self.update_buttons()


class Button:
    def __init__(self, ds, size, id, img, data):
        self.ds = ds
        self.width, self.height = size
        self.y = 0
        self.id = id
        self.img = img
        self.colour = get_random_colour()
        self.data = data
        self.text = Text('fonts/font_shop16.png', 2, 2)

        self.text_offsets = {
            1: 40,
            2: 33,
            3: 27,
            4: 22
        }
        self.prefixes = {
            1000: "k",
            1000000: "m"
        }

    def render(self, scroll, shop_position):
        if shop_position[0] != DISPLAY_SIZE[0]:
            self.y = ((shop_position[1] + 8) + self.id * 96) - scroll
            if -84 < self.y < DISPLAY_SIZE[1]:
                if self.img is None:
                    pygame.draw.rect(self.ds, self.colour, (shop_position[0] + 8, self.y, self.width, self.height))
                else:
                    self.ds.blit(self.img, (shop_position[0] + 8, self.y))

                if self.data != None:
                    text = self.convert_to_prefixes(self.data["cost"])
                    x_offset = self.text_offsets[len(text)]
                    self.text.render(self.ds, text, (shop_position[0] + (8 + x_offset), self.y + 61))

    def convert_to_prefixes(self, data):
        output = ''
        if data > 1000:
            for prefix in self.prefixes.keys():
                comparison = data / prefix
                if 1 < comparison < 1000:
                    output += str(int(data / prefix))
                    output += self.prefixes[prefix]
        else:
            output = str(data)
        return output

    def update(self, scroll, shop_position):
        self.render(scroll, shop_position)
