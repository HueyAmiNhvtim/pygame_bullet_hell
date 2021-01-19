import pygame
import numpy
from pygame.sprite import Sprite
from pygame import Vector2
from straight_pattern import StraightPattern
from tri_pattern import TriPattern
from collections import deque
# TO-DO: Delay each sprite's action until time...
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

        # Vector-based movement
        self.vector = Vector2()
        self.normalized_vector = Vector2()
        self.destination = [0, 0]

        # cooldown and last_time stuff
        self.movement_cooldown = self.settings.movement_cooldown
        self.last_time = pygame.time.get_ticks()

        # Area allowed to move around.
        self.boundary_x = (0, self.settings.screen_width - self.rect.width + 1)
        self.boundary_y = (self.rect.y, self.settings.screen_height - self.rect.height + 1)

        # Flags
        self.movement_disabled = False

        # Placeholder pattern
        self.first_pattern = StraightPattern(main_game, self)
        self.second_pattern = TriPattern(main_game, self)

    def update(self):
        """This is where the alien will move. Will need to fix if reached destination"""
        self.first_pattern.shoot_burst()
        self._check_if_passed_destination()
        if self.movement_disabled is False:
            self.x += self.normalized_vector[0] * self.settings.alien_speed
            self.y += self.normalized_vector[1] * self.settings.alien_speed
            self.rect.x = self.x
            self.rect.y = self.y
            self.last_time = pygame.time.get_ticks()

    def create_destination_and_vector(self):
        """Upon creation of alien and when alien reaches a destination, create a new one"""
        self.destination[0] = numpy.random.randint(0, self.boundary_x[1])
        self.destination[1] = numpy.random.randint(self.boundary_y[0], self.boundary_y[1])
        self.vector[0] = self.destination[0] - self.rect.x
        self.vector[1] = self.destination[1] - self.rect.y
        self.normalized_vector = self.vector.normalize()

    def _check_if_passed_destination(self):
        time_now = pygame.time.get_ticks()
        # Use Vector to calculate the distance between the alien and the destination
        dist_between_ob_dis = Vector2(self.destination[0] - self.rect.x, self.destination[1] - self.rect.y).magnitude()
        # Alien_speed will act as a proximity surrounding the destination.
        if dist_between_ob_dis <= self.settings.alien_speed:
            if time_now - self.last_time >= self.movement_cooldown:
                self.create_destination_and_vector()
                self.movement_disabled = False
            else:
                self.movement_disabled = True

    def health_tooltip(self):
        """Display health on top of the alien."""
        pass
