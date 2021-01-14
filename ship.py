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
        self.ship_rect = self.image.get_rect()
        self.rect = self.core.get_rect()

        # Start the ship at the middle bottom of the screen. Place the core in the middle of the ship
        self.ship_rect.midbottom = self.screen_rect.midbottom
        self.rect.centerx = self.ship_rect.centerx
        self.rect.top = self.ship_rect.top + 5

        # Store decimal values for the ship positions
        self.x = float(self.ship_rect.x)
        self.y = float(self.ship_rect.y)

    def draw_ship(self):
        self.screen.blit(self.image, self.ship_rect)
        self.screen.blit(self.core, self.rect)

    def update(self):
        """Full movement in 2D space whoop. Will add Shift for slower movement later"""
        # Up - Left, Down-Right not firing bullets for some reason...
        # The above problem is due to ghosting issues on the keyboard...
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and self.ship_rect.right <= self.screen_rect.right:
            self._update_vertical(keys)
            self.x += 1 * self.settings.ship_speed
        elif keys[pygame.K_a] and self.ship_rect.left >= self.screen_rect.left:
            self._update_vertical(keys)
            self.x -= 1 * self.settings.ship_speed
        elif keys[pygame.K_w] and self.ship_rect.top >= self.screen_rect.top:
            self.y -= 1 * self.settings.ship_speed
        elif keys[pygame.K_s] and self.ship_rect.bottom <= self.screen_rect.bottom:
            self.y += 1 * self.settings.ship_speed
        self.ship_rect.x = self.x
        self.ship_rect.y = self.y
        self.rect.centerx = self.ship_rect.centerx
        self.rect.top = self.ship_rect.top + 5

    def _update_vertical(self, keys):
        if keys[pygame.K_w] and self.ship_rect.top >= self.screen_rect.top:
            self.y -= 1 * self.settings.ship_speed
        elif keys[pygame.K_s] and self.ship_rect.bottom <= self.screen_rect.bottom:
            self.y += 1 * self.settings.ship_speed

    def respawn_ship(self):
        """When ship is hit, respawn it at the midbottom of the screen.
        In the future, will give invisbility_time. Maybe do some blinking as well."""
        self.ship_rect.midbottom = self.screen_rect.midbottom
        self.rect.centerx = self.ship_rect.centerx
        self.rect.y = self.ship_rect.y + 5
        self.x = float(self.ship_rect.x)
        self.y = float(self.ship_rect.y)
