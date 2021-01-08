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

# pygame.key.set_repeat(1, 50)  # Allowing repeat per 50 milliseconds
while True:
    keys = pygame.key.get_pressed() # a list of state of each key on the keyboard
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # if event.type == pygame.KEYDOWN:
            # if event.key == K_ESCAPE:
                # pygame.quit()
                # sys.exit()
            # if event.key == K_RIGHT:
                # coin_x += dx
        # if event.type == pygame.MOUSEBUTTONDOWN:
        postition = pygame.mouse.get_pos()  # List of 2 values - x, y
        coin_x = postition[0] - coin_rect.width // 2
        coin_y = postition[1] - coin_rect.height // 2
    if keys[K_RIGHT]:
        coin_x += dx
    elif keys[K_UP]:
        coin_y -= dy
    elif keys[K_LEFT]:
        coin_x -= dx
    elif keys[K_DOWN]:
        coin_y += dy

    screen.fill((100, 25, 47))  # Clear the screen by repainting it.
    # Move the image
    # coin_x += dx
    # coin_y += dy
    if coin_x < 0:
        coin_x = 0
    elif coin_x + coin_rect.width > screen_rect.width:
        coin_rect.right = screen_rect.right
    if coin_y < 0:
        coin_y = 0
    elif coin_y + coin_rect.height > screen_rect.height:
        coin_rect.bottom = screen_rect.bottom
    screen.blit(coin_screen, (coin_x, coin_y))
    # Buffering the drawing to reduce flickers
    pygame.display.flip()
    pygame.display.update()
    fps_clock.tick(FPS)

