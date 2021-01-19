import pygame
from pygame.sprite import Sprite
from pygame import Vector2


class BulletAlienUno(Sprite):
    """Bullet for the alien. First time using spritesheet"""
    """I'm guessing that each class is for different patterns"""
    def __init__(self, main_game, shooter):
        """Initialize attributes for the alien's boolets"""
        super().__init__()
        self.screen = main_game.screen
        self.settings = main_game.settings
        self.image = main_game.al_bullet_one
        self.bullet_hitbox = pygame.Surface(size=(6, 6))  # True hitbox of bullet for some sick bullet dodging
        self.bullet_rect = self.bullet_hitbox.get_rect()
        self.mask = pygame.mask.from_surface(self.bullet_hitbox)

        # Start each bullet out of the alien. This is where the alien will shoot the pattern
        self.rect = self.image.get_rect()
        self.rect.midtop = shooter.rect.midbottom
        self.bullet_rect.center = self.rect.center

        # Vector movement for the bullet
        self.vector = Vector2()
        self.normalized_vector = Vector2()
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def draw_bullet(self):
        """Draw the boolet"""
        self.screen.blit(self.bullet_hitbox, self.bullet_rect)
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Generic bullet update in 2D"""
        # print(self.rect.midtop)
        self.x += self.normalized_vector[0] * self.settings.ali_bullet_speed
        self.y += self.normalized_vector[1] * self.settings.ali_bullet_speed
        self.rect.x = self.x
        self.rect.y = self.y
        self.bullet_rect.center = self.rect.center


class BulletAlienDos(BulletAlienUno):
    """Exactly same class, just with different image"""
    def __init__(self, main_game, shooter):
        super().__init__(main_game, shooter)
        self.image = main_game.al_bullet_two


class BulletAlienTres(BulletAlienUno):
    """Exactly same class, just with different image"""
    def __init__(self, main_game, shooter):
        super().__init__(main_game, shooter)
        self.image = main_game.al_bullet_three

