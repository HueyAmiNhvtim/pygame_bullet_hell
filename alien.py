import pygame
import numpy
from pygame.sprite import Sprite
from pygame import Vector2
# TO-DO: Maybe do sth like this:
# Set a random point within the boundary of the screen.
# Create a vector heading towards that point.
# Head using the speed specified in the settings. I suppose you can can used magnitude as
# the speed of the alien, which should conform with the settings.
# Once reached, spam boolets and then move to a new position.


class Alien(Sprite):
    def __init__(self, main_game):
        super(Alien, self).__init__()
        self.screen = main_game.screen
        self.settings = main_game.settings

        self.image = pygame.image.load("images/alien_ph.bmp")
        self.rect = self.image.get_rect()

        self.mask = pygame.mask.from_surface(self.image.convert_alpha())
        self.rect.x = self.rect.width // 5
        self.rect.y = self.rect.height * 2

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.health = self.settings.alien_health

    def update(self):
        pass

    def health_tooltip(self):
        """Display health on top of the alien."""
        pass
