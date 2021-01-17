import pygame
from pygame.sprite import Sprite


class BulletAlien(Sprite):
    """Bullet for the alien. First time using spritesheet"""
    """I'm guessing that each class is for different patterns"""
    def __init__(self, main_game, alien):
        """Initialize attributes for the alien's boolets"""
        super().__init__()
        self.screen = main_game.screen
        self.settings = main_game.settings
        self.shooter = alien
        self.image = None
        self.color = ''

        # Start each bullet out of the alien. This is where the alien will shoot the pattern
        self.rect = self.image.get_rect()
        self.midbottom = alien.rect.midtop

        self.y = float(self.rect.y)

    def draw_bullet(self):
        """Draw the boolet"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """This is where different patterns have different kinds of update, huh"""
        self.y -= self.settings.ali_bullet_speed
        self.rect.y = self.y

