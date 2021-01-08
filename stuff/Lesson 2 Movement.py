import pygame
import sys
from pygame.locals import *
# This is gonna go bad for me...

width = 1024
height = 720
FPS = 30  # chanes the speed of the animation
fps_clock = pygame.time.Clock()  # Clock function to time animation

# Complicated can have multiple surfaces
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("First Pygame")

coin_screen = pygame.image.load("img.png")
coin_x = 20
coin_y = 60
dx = 1
dy = 1

# set screen and coin_screen into rect objects
screen_rect = screen.get_rect()
coin_rect = coin_screen.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((100, 25, 47))  # Clear the screen by repainting it.
    # Move the image
    coin_x += dx
    coin_y += dy
    if coin_x + coin_rect.width > screen_rect.width or coin_x < 0:
        dx *= -1
    if coin_y + coin_rect.height > screen_rect.height or coin_y < 0:
        dy *= -1
    screen.blit(coin_screen, (coin_x, coin_y))
    # Buffering the drawing to reduce flickers
    pygame.display.flip()
    pygame.display.update()

