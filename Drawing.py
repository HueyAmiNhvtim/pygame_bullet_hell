import pygame
import sys
from pygame.locals import *
# This is gonna go bad for me...

width = 1024
height = 768

# Complicated can have multiple surfaces
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("First Pygame")

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((0, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (300, 50), 20)
    pygame.draw.line(screen, (255, 255, 255), (100, 100), (500, 500), 65)
    pygame.draw.polygon(screen, (255, 0, 0), ((146, 0), (291, 186), (236, 277), (56, 277), (0, 186)))
    # Buffering the drawing to reduce flickers
    pygame.display.flip()
    pygame.display.update()
