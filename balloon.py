import pygame
import time
from support import get_random_colour, load_json
from random import choice, randint
from settings import *

class BalloonManager:
    def __init__(self, ds):
        self.ds = ds

        pygame.mixer.init()
        path = 'sounds/balloon/'
        self.explosion_sounds = ['balloon1', 'balloon2', 'balloon3', 'balloon4']
        self.explosion_sounds = [pygame.mixer.Sound(f'{path}{sound}.wav') for sound in self.explosion_sounds]

        self.balloons = []
        self.balloon_count = 0
        self.balloon_order = []

        self.start_time = time.time()
        self.timers = {
            "balloon_timer": self.start_time,
            "wave_timer": self.start_time
        }
        self.wave_time = 5
        self.on_wave = False
        self.time_per_balloon = 1
        self.balloon_speed = 50

        self.wave_data = load_json('data/wave')
        self.wave = 0

    def check_time(self):
        current_time = time.time()
        if not self.on_wave:
            if current_time > self.timers['wave_timer'] + 1:
                self.wave_time -= 1
                self.timers['wave_timer'] = current_time
                if self.wave_time <= 0:
                    self.on_wave = True
                    self.wave += 1
                    current_wave_data = self.wave_data[f"wave {self.wave+1}"]
                    self.wave_time = current_wave_data["shop_period"]
                    self.time_per_balloon = current_wave_data["time"]
                    self.balloon_speed = current_wave_data["speed"]

                    b_data = self.wave_data[f"wave {self.wave}"]["balloons"]
                    # Total balloon count
                    for balloon_type in b_data:
                        self.balloon_count += balloon_type[0]
                    # Get order and damages
                    self.balloon_order = []
                    for balloon_type in b_data:
                        for balloon in range(balloon_type[0]):
                            self.balloon_order.append(balloon_type[1])

        else:
            if self.balloon_count != 0:
                if current_time > self.timers["balloon_timer"] + self.time_per_balloon:
                    type = choice(self.balloon_order)
                    self.spawn_balloon(type)
                    self.balloon_order.remove(type)
                    self.timers["balloon_timer"] = current_time
            elif len(self.balloons) == 0:
                self.on_wave = False


        return [self.wave, self.wave_time, self.on_wave]

    def spawn_balloon(self, dmg):
        self.balloons.append(Balloon(self.ds, 'normal', self.balloon_speed, (randint(89, 518), -20), dmg))
        self.balloon_count -= 1

    def update_balloons(self, dt):
        out = 0
        for balloon in self.balloons:
            balloon.update(dt)
            if balloon.y > DISPLAY_SIZE[1] + 48:
                out += balloon.health * 3
                self.balloons.remove(balloon)
        return out

    def check_collisions(self, mouse_position, damage, aoe):
        mouseX, mouseY = mouse_position[0], mouse_position[1]
        for balloon in self.balloons:
            # Create a mini 8x8 rect around the mouse as a buffer so clicking isn't so frustrating
            if balloon.rect.colliderect((mouseX - aoe * 0.5, mouseY - aoe * 0.5, aoe, aoe)):
                balloon.health -= damage
                if balloon.health <= 0:
                    choice(self.explosion_sounds).play()
                    self.balloons.remove(balloon)
                else:
                    balloon.original_colour = balloon.colour_index[balloon.health]
                balloon.hit = True
                # if damage is more than the balloons initial health you only get that amount of money
                if damage > balloon.max_health:
                    damage = balloon.max_health
                return damage
        return 0

class Balloon:
    def __init__(self, ds, type, speed, pos, health):
        self.ds = ds
        self.type = type
        self.x, self.y = pos
        self.size = 20
        self.speed = speed

        self.max_health = health
        self.health = self.max_health

        self.hit = False

        self.colour_index = {
            1: (255, 0, 0),
            2: (0, 0, 255),
            3: (0, 255, 0),
            4: (255, 255, 0),
            5: (255, 105, 180)
        }

        self.original_colour = self.colour_index[self.max_health]

        self.colour = self.original_colour
        self.start_time = time.time()
        self.hit_timer = self.start_time

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def hit_effect(self):
        current_time = time.time()
        if self.hit:
            self.hit_timer = current_time
            self.colour = (255, 255, 255)
            self.hit = False

        if current_time > self.hit_timer + 0.1:
            self.colour = self.original_colour

    def move(self, dt):
        self.y += self.speed * dt
        # self.x += -6 * dt
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def render(self):
        pygame.draw.rect(self.ds, self.colour, (self.x, self.y, self.size, self.size))

    def update(self, dt):
        self.move(dt)
        self.hit_effect()
        self.render()