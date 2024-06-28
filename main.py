import pygame
from game import Game
from settings import *

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.surface.Surface(DISPLAY_SIZE)
clock = pygame.time.Clock()
TITLE = "Pyhunt 2 "

icon_img = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon_img)

game = Game(display)

#WINDOW_SIZE = (1920, 1080)
#screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)

while True:
	dt = clock.tick(FPS) * .001
	game.update(dt)
	pygame.display.set_caption(TITLE + str(clock.get_fps()))
	surf = pygame.transform.scale(display, WINDOW_SIZE)
	screen.blit(surf, (0, 0))
	pygame.display.update()