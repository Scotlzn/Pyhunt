import pygame
from text import Text

class UserInterfaceManager:
    def __init__(self, ds, game):
        self.ds = ds
        self.game = game

        self.wave_data = []

        self.test = Text('fonts/font_white16.png', 2, 3)
        self.test2 = Text('fonts/font_white32.png', 4, 1)

    def render_board(self):
        pygame.draw.rect(self.ds, '#eb8034', (2, 2, 87, 20))
        pygame.draw.rect(self.ds, '#9c4b11', (2, 2, 87, 20), 2)

    def render_text(self, dt):
        # pygame.draw.rect(self.ds, (255,0,0), (320, 0, 1, 360)) # centered red line
        self.test.render(self.ds, f'Money: {self.game.money}', (5, 5))
        if self.wave_data[2]:
            self.test2.render(self.ds, f'Wave {self.wave_data[0]}', (280, 4))
        else:
            self.test2.render(self.ds, f'Wave {self.wave_data[0] + 1} starts in {self.wave_data[1]}', (180, 4))



    def update(self, dt):
        self.render_board()
        self.render_text(dt)