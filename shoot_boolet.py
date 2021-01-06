import pygame
from pygame.locals import *
import sys
from boolet import Boolet


class Coin(object):
    def __init__(self, x, y, dx, dy, background):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.surface = pygame.image.load("snowflake.bmp")
        self.coin_rect = self.surface.get_rect()
        self.background = background
        self.backrect = self.background.get_rect()

    def move_with_mouse(self):
        mouse_position = pygame.mouse.get_pos()
        self.x = mouse_position[0] - nu_coin.coin_rect.width // 2  # LEFT
        self.y = mouse_position[1] - nu_coin.coin_rect.height // 2  # TOP

    def shoot_boolet(self):
        mouse_pressed = pygame.mouse.get_pressed(num_buttons=3)
        if mouse_pressed[0]:
            boolet = Boolet(screen, self)  # Oh yeah, you can use self alone... Why do I keep forgetting this?
            boolet.boolet_move()

    def blit_ship(self):
        self.background.blit(self.surface, (self.x, self.y))


width = 800
height = 600
size = 248
FPS = 20  # control the speed of animation
fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((width,height))
screen_rect = screen.get_rect()
nu_coin = Coin(0, 0, 1, 1, screen)
pygame.display.set_caption("First Pygame")


while True:
    for event in pygame.event.get():
        if event.type == QUIT: #when the user closes the window
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    screen.fill((100, 25, 47))  # clears the screen by repainting it
    nu_coin.move_with_mouse()
    nu_coin.shoot_boolet()
    nu_coin.blit_ship()
    pygame.display.update()
    fpsClock.tick(FPS)
