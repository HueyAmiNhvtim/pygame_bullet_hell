import pygame
import sys
from pygame.locals import *
import pygame
import sys
from pygame.locals import *
# This is gonna go bad for me...

width = 1024
height = 768
y = 0
x = 0
y_dir = 1
x_dir = 1

# Complicated can have multiple surfaces
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("First Pygame")

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((0, 255, 255))  # Clear the screen by repainting it.
    pygame.draw.line(screen, (255, 0, 0), (0, y), (width, y), 2)
    pygame.draw.line(screen, (255, 0, 0), (x, 0), (x, height), 2)

    # The line moves kinda wack.
    pygame.draw.line(screen, (255, 0, 0), (x, 0), (height, x), 2)
    y += y_dir
    x += x_dir
    if y == 0 or y == height:
        y_dir *= -1

    if x == 0 or x == width:
        x_dir *= -1
    # Buffering the drawing to reduce flickers
    pygame.display.flip()
    pygame.display.update()

