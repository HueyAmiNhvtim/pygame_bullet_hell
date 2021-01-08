import pygame
from pygame.sprite import Sprite
import sys
import random as rdn


class Snowflake(Sprite):
    def __init__(self, x, y, spood, background):
        super().__init__()
        self.y = y
        self.surface = pygame.image.load("snowflake.bmp")
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.background = background
        self.speed = spood

    def update(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw_snow(self):
        self.background.blit(self.surface, self.rect)


width = 1200
height = 600
size = 49
FPS = 20  # control the speed of animation
fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("First Pygame")

my_snows = pygame.sprite.Group()
for i in range(width // size + 1):
    x = i * size
    y = 0
    speed = 2 * (i + 1)
    print(speed)
    my_snows.add(Snowflake(x, y, speed, screen))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #when the user closes the window
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    screen.fill((100, 25, 47))  # clears the screen by repainting it
    my_snows.update()
    # Update position, then check, then draw if passed.
    for snow in my_snows:
        if snow.rect.y > screen.get_height():
            snow.y = 0
    for snow in my_snows:
        snow.draw_snow()
    pygame.display.flip()
    fpsClock.tick(FPS)