import pygame, sys
from pygame.locals import *
import random as rdn


class Coin(object):
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.surface = pygame.image.load("img.png")

    def move(self, background):
        screenRect = screen.get_rect()
        coinRect = self.surface.get_rect()
        self.x += self.dx
        self.y += self.dy
        #check to see if going off the screen
        if self.x < 0:
            self.dx *= -1
        if self.x + coinRect.width > screenRect.width:
            self.dx *= -1
        if self.y < 0:
            self.dy *= -1
        if self.y + coinRect.height > screenRect.height:
            self.dy *= -1


width = 800
height = 600
size = 248
FPS = 20 #control the speed of animation
fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("First Pygame")

#myCoin = Coin(100,100,3,3) #(x,y) (speedx, speedy)
my_coins = []
for i in range(5):
    x = rdn.randint(0, width - size)
    y = rdn.randint(0, height - size)
    my_coins.append(Coin(x, y, i+1, i+1))

while True:
    for event in pygame.event.get():
        if event.type == QUIT: #when the user closes the window
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    screen.fill((100,25,47)) #clears the screen by repainting it
    for c in my_coins:
        screen.blit(c.surface, (round(c.x), round(c.y)))
        c.move(screen)
    pygame.display.update()
    fpsClock.tick(FPS)