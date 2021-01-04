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
    wat = 0
    times = 5
    #pygame.draw.circle(screen, (255, 0, 0), (300, 50), 20)
    # 1024, 1 => 1023, 2 => 1022, 3
    #for i in range(width):
        #pygame.draw.line(screen, (255, 0, 0), (width - i, 0), (0, wat + 1))
        #wat += 1

    for i in range(width // times):
        pygame.draw.line(screen, (255, 0, 0), (width - i * times, 0), (0, wat + i * times))
        wat += 1
    #pygame.draw.line(screen, (255, 0, 0), (width / 2, 0), (width / 2, height))
    #pygame.draw.line(screen, (255, 0, 0), (0, height / 2), (width, height / 2))
    #pygame.draw.line(screen, (0, 100, 0), (0, 0), (width, height))
    #pygame.draw.line(screen, (0, 100, 0), (width, 0), (0, height))
    #pygame.draw.polygon(screen, (255, 0, 0), ((146, 0), (291, 186), (236, 277), (56, 277), (0, 186)))
    # Buffering the drawing to reduce flickers
    pygame.display.flip()
    pygame.display.update()
