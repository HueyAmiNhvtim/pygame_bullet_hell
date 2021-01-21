import pygame
import numpy
from pygame.sprite import Sprite
from pygame import Vector2
from pattern_manager import PatternManager
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
        self.actual_rect = self.rect
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
        self.shoot = True  # Disable shooting after exhausting the current pattern's burst
        self.confirmed_switch = True  # Confirming that a switch has taken place

        # Initiating pattern manager
        self.pattern_manager = PatternManager(main_game, self)

        # For the health tooltip:
        self.bar_width, self.bar_height = (25, 25)
        self.bar_surface = pygame.Surface((self.bar_width, self.bar_height))
        self.bar_surface.set_alpha(0)
        self.text_color = (0, 255, 255)
        self.font = pygame.font.Font("font/edosz.ttf", 24)

        self.bar_rect = pygame.Rect(0, 0, self.bar_width, self.bar_height)
        self.bar_rect.midbottom = self.rect.midtop
        self.update_health()

    def update(self):
        """This is where the alien will move. Will need to fix if reached destination"""
        self.pattern_manager.use_pattern()
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
        if self.confirmed_switch and dist_between_ob_dis <= self.settings.alien_speed:
            self.movement_disabled = True
            # Make sure that the manager does not constantly switch pattern while object stops
            self.confirmed_switch = False
            self.pattern_manager.switch_pattern()
        if time_now - self.last_time >= self.movement_cooldown:
            self.create_destination_and_vector()
            self.pattern_manager.switch_pattern()
            self.movement_disabled = False
            self.confirmed_switch = True  # Reactivate the flag so that the alien can switch pattern again.

    def update_health(self):
        """Display health on top of the alien."""
        self.bar_rect.midbottom = self.rect.midtop
        self.health_display = self.font.render(str(self.health), True, self.text_color, None)
        self.health_rect = self.health_display.get_rect()
        self.health_rect.center = self.bar_rect.center

    def draw_bar_health(self):
        self.screen.blit(self.bar_surface, self.bar_rect)
        self.screen.blit(self.health_display, self.health_rect)
