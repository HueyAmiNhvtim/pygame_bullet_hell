import pygame
import numpy
from pygame.sprite import Sprite
from pygame import Vector2


class Alien(Sprite):
    def __init__(self, main_game):
        super(Alien, self).__init__()
        self.screen = main_game.screen
        self.settings = main_game.settings

        self.image = pygame.image.load("images/alien_ph.bmp")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width // 5
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        pass

