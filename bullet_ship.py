import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, main_game):
        super().__init__()
        self.screen = main_game.screen
        self.settings = main_game.settings
        self.color = self.settings.bullet_color

        # Bullet as a rect object... First created it in 0,0, then correct the position.
        # ehh, it should be fast enough to not be noticeable
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = main_game.ship.rect.midtop

        # Store the bullet's position for easier calculation and accessibility. Will have to update
        # the rect, too.
        self.y = float(self.rect.y)

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def update(self):
        """Update the position of the bullet, then update the rect version"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
