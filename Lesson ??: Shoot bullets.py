import pygame
from pygame.locals import *
import sys
import random as rdn

vec = pygame.math.Vector2


class Cannon(pygame.sprite.Sprite):
    def __init__(self, main_screen):
        super().__init__()  # Inherit the Sprite class's variables
        self.image = pygame.image.load("Snowflake.bmp")
        self.rect = self.image.get_rect()
        self.screen = main_screen
        self.rect.midbottom = main_screen.get_rect().midbottom

    def update(self):
        position = pygame.mouse.get_pos()  # Returns mouse pointer positions
        self.rect.x = position[0]


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("snowflake.bmp")
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 3


class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("snowflake.bmp")
        self.rect = self.image.get_rect()


width = 800
height = 600
size = 248
screen = pygame.display.set_mode((width, height))
screen_rect = screen.get_rect()

sprite_list = pygame.sprite.Group()
target_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()


# create a list of targets
c1 = Cannon(screen)

for i in range(10):
    target = Target()
    target.rect.x = rdn.randint(0, width - target.rect.width)
    target.rect.y = rdn.randint(0, height - c1.rect.height)
    sprite_list.add(target)
    target_list.add(target)

sprite_list.add(c1)  # Add the list to the list of all sprites
FPS = 30  # control the speed of animation
fpsClock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT: #when the user closes the window
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            bullet = Bullet()
            bullet.rect.midbottom = c1.rect.midtop
            sprite_list.add(bullet)
            bullet_list.add(bullet)
    sprite_list.update()  # All of the sprites inside the group has to have the update method
    screen.fill((10, 25, 47))

    # collision detection
    for bullet in bullet_list:
        hit_list = pygame.sprite.spritecollide(bullet, target_list, True)
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            sprite_list.remove(bullet)
        for hit in hit_list:
            bullet_list.remove(bullet)
            sprite_list.remove(bullet)
    print(len(bullet_list))
    # draw all the sprites and update the display
    sprite_list.draw(screen)
    pygame.display.flip()
    fpsClock.tick(FPS)
