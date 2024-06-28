import pygame, sys
from particles import ParticleManager
from background import BackgroundManager
from balloon import BalloonManager
from ui import UserInterfaceManager
from shop import ShopManager
from save import SaveManager
from support import fix_mouse, get_shop_button_pressed, load_json, save_json

class Game:
    def __init__(self, ds):
        self.ds = ds

        self.ui_manager = UserInterfaceManager(self.ds, self)
        self.shop_manager = ShopManager(self.ds)
        self.particle_manager = ParticleManager(self.ds)
        self.background_manager = BackgroundManager(self.ds)
        self.balloon_manager = BalloonManager(self.ds)
        self.save_manager = SaveManager()

        self.shop = False

        savedata = self.save_manager.load()
        self.money = savedata[0]
        self.damage = savedata[1]
        self.aoe = savedata[2]

    def quit_game(self):
        self.save_manager.save(["money", "damage", "aoe"], [self.money, self.damage, self.aoe])
        pygame.quit()
        sys.exit()

    def eventloop(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_position = fix_mouse(event.pos)
                    if mouse_position[0] < 540 or not self.shop:
                        self.particle_manager.create_particles(mouse_position)
                        collision = self.balloon_manager.check_collisions(mouse_position, self.damage, self.aoe)
                        if collision != 0:
                            self.money += collision
                    elif self.shop_manager.active:
                        button = get_shop_button_pressed(mouse_position, self.shop_manager.scroll)
                        if button != -1:
                            if button in [0, 1, 2]:
                                self.upgrade(button)

                if event.button == 3 and not self.shop_manager.moving:
                    self.shop = not self.shop

                # Only be able to scroll when to shop is open and not moving
                if self.shop_manager.active:
                    # 4 is up 5 is down
                    if event.button == 4:
                        self.shop_manager.scroll += -500 * dt
                    if event.button == 5:
                        self.shop_manager.scroll += 500 * dt


    def upgrade(self, button):

        def calculate_cost(money, c):
            if money > c:
                money -= c
                self.shop_manager.upgrade_sound.play()
                return [money, True]
            self.shop_manager.denied_sound.play()
            return [money, False]

        b_object = self.shop_manager.buttons[button]
        cost = b_object.data["cost"]
        if button == 0:
            self.money, can_buy = calculate_cost(self.money, cost)
            if can_buy: self.damage += 1
        elif button == 1:
            self.money, can_buy = calculate_cost(self.money, cost)
            if can_buy: self.aoe += 2
        elif button == 2:
            self.money, can_buy = calculate_cost(self.money, cost)

    def update(self, dt):
        self.eventloop(dt)
        self.background_manager.update(dt)

        # get wave data and check on wave and send to ui
        wave_data = self.balloon_manager.check_time()
        self.ui_manager.wave_data = wave_data

        money_lost = self.balloon_manager.update_balloons(dt)
        if money_lost != 0:
            self.money -= money_lost
            if self.money < 0:
                pass
                # print('BANKRUPT! YOU LOST')

        self.particle_manager.update(dt)
        self.ui_manager.update(dt)
        self.shop_manager.update(dt, self.shop)