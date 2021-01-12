import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, main_game_class):
        """Initialize the ship and its starting positions"""
        super().__init__()

        # Load parent's class necessary attributes. I think that is a correct term for it...
        self.screen = main_game_class.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = main_game_class.settings

        self.image = pygame.image.load("images/ship.bmp")
        self.core = pygame.image.load("images/core.bmp")
        self.rect = self.image.get_rect()
        self.core_rect = self.core.get_rect()

        # Start the ship at the middle bottom of the screen. Place the core in the middle of the ship
        self.rect.midbottom = self.screen_rect.midbottom
        self.core_rect.centerx = self.rect.centerx
        self.core_rect.y = self.rect.y - 5

        # Store decimal values for the ship positions
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def draw_ship(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.core, self.core_rect)

    def update(self):
        """Full movement in 2D space whoop. Will add Shift for slower movement later"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right <= self.screen_rect.right:
            if keys[pygame.K_UP] and self.rect.top >= self.screen_rect.top:
                self.y -= 1 * self.settings.ship_speed
            if keys[pygame.K_DOWN] and self.rect.bottom <= self.screen_rect.bottom:
                self.y += 1 * self.settings.ship_speed
            self.x += 1 * self.settings.ship_speed
        elif keys[pygame.K_LEFT] and self.rect.left >= self.screen_rect.left:
            if keys[pygame.K_UP] and self.rect.top >= self.screen_rect.top:
                self.y -= 1 * self.settings.ship_speed
            if keys[pygame.K_DOWN] and self.rect.bottom <= self.screen_rect.bottom:
                self.y += 1 * self.settings.ship_speed
            self.x -= 1 * self.settings.ship_speed
        elif keys[pygame.K_UP] and self.rect.top >= self.screen_rect.top:
            self.y -= 1 * self.settings.ship_speed
        elif keys[pygame.K_DOWN] and self.rect.bottom <= self.screen_rect.bottom:
            self.y += 1 * self.settings.ship_speed
        self.rect.x = self.x
        self.rect.y = self.y
        self.core_rect.centerx = self.rect.centerx
        self.core_rect.top = self.rect.top + 5
