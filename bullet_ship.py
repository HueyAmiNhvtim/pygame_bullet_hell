import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, main_game):
        super().__init__()
        self.screen = main_game.screen
        self.settings = main_game.settings
        # self.color = self.settings.bullet_color

        # Bullet as a rect object... First created it in 0,0, then correct the position.
        # ehh, it should be fast enough to not be noticeable
        self.image = main_game.ship_bullet
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())
        self.rect.midtop = main_game.ship.ship_rect.midtop

        # Store the bullet's position for easier calculation and accessibility. Will have to update
        # the rect, too.
        self.y = float(self.rect.y)

    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the position of the bullet, then update the rect version"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
