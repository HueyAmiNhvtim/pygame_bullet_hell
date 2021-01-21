import pygame
from pygame.sprite import Sprite


class Bomb(Sprite):
    def __init__(self, main_game):
        super().__init__()
        self.main_game = main_game
        self.screen = main_game.screen
        self.settings = main_game.settings
        # self.color = self.settings.bullet_color

        # Bullet as a rect object... First created it in 0,0, then correct the position.
        # ehh, it should be fast enough to not be noticeable
        self.image = main_game.bomb_ship
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())
        self.rect.center = main_game.ship.ship_rect.center

        # BOMB settings
        self.bomb_duration = self.settings.bomb_time
        self.update_tick = self.settings.bomb_update_tick
        self.expand_rate = self.settings.expand_rate

        # Store the bullet's position for easier calculation and accessibility. Will have to update
        # the rect, too.
        self.y = float(self.rect.y)

        # Flags
        self.bomb = True
        self.expandable = False
        # Time
        self.start_time = pygame.time.get_ticks()
        self.last_update = pygame.time.get_ticks()

    def draw_bomb(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self._check_bomb_duration()
        if self.bomb:
            self._check_if_expandable()
            if self.expandable:
                self._expand_bomb()
                self.last_update = pygame.time.get_ticks()

    def _check_bomb_duration(self):
        now = pygame.time.get_ticks()
        if now - self.start_time >= self.bomb_duration:
            self.bomb = False

    def _check_if_expandable(self):
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.update_tick:
            self.expandable = True

    def _expand_bomb(self):
        """Update the position of the bullet, then update the rect and mask version"""
        new_width, new_height = self.rect.width + self.expand_rate, self.rect.height + self.expand_rate
        self.image = pygame.transform.smoothscale(self.image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.center = self.main_game.ship.ship_rect.center
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())