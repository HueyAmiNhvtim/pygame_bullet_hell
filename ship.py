import pygame
import math
from pygame.sprite import Sprite
from bullet_ship import Bullet
# There's a bug in invincibilty frame...


class Ship(Sprite):
    def __init__(self, main_game_class):
        """Initialize the ship and its starting positions"""
        super().__init__()
        # Load parent's class necessary attributes. I think that is a correct term for it...
        self.main_game = main_game_class
        self.screen = self.main_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = self.main_game.settings

        self.image = pygame.image.load("images/ship.bmp")
        self.core = pygame.image.load("images/core.bmp")
        self.ship_rect = self.image.get_rect()
        self.rect = self.core.get_rect()
        # self.bombs = self.settings.bomb_limit

        # Start the ship at the middle bottom of the screen. Place the core in the middle of the ship
        self.ship_rect.midbottom = self.screen_rect.midbottom
        self.rect.centerx = self.ship_rect.centerx
        self.rect.top = self.ship_rect.top + 5
        self.hit_box_surface = pygame.Surface(size=(4, 4))
        self.hit_box = self.hit_box_surface.get_rect()

        # Mask for the true tiny hitbox of 4px
        self.mask = pygame.mask.from_surface(self.core)

        # Store decimal values for the ship positions
        self.x = float(self.ship_rect.x)
        self.y = float(self.ship_rect.y)

        # Flags:
        self.god_mode = False
        self.start_respawn_time = pygame.time.get_ticks()

        # Invisibility settings
        self.alpha = 255  # 255: opaque, 0: transparent
        self.god_time = self.settings.god_time
        self.frame_timer = 0  # For decreasing and increasing alpha
        self.alpha_modifier = 255 // (self.settings.FPS // 4)
        self.up = False  # Boolean to detect whether to increase opacity or not

        # Shoot bullet attributes
        self.bullet_cooldown = self.settings.ship_bullet_cooldown
        self.shoot_disabled = False
        self.last_bullet_fired = pygame.time.get_ticks()

    def update(self):
        """Full movement in 2D space whoop. Will add Shift for slower movement later"""
        # Up - Left, Down-Right not firing bullets for some reason...
        # The above problem is due to ghosting issues on the keyboard...
        keys = pygame.key.get_pressed()
        self._movement_update(keys)
        self._shoot_update(keys)
        self.ship_rect.x = self.x
        self.ship_rect.y = self.y
        self.rect.centerx = self.ship_rect.centerx
        self.rect.top = self.ship_rect.top + 5
        self.hit_box.center = self.rect.center

    def _movement_update(self, keys):
        if keys[pygame.K_d] and self.rect.right <= self.screen_rect.right:
            self._update_vertical(keys)
            self.x += 1 * self.settings.ship_speed
        elif keys[pygame.K_a] and self.rect.left >= self.screen_rect.left:
            self._update_vertical(keys)
            self.x -= 1 * self.settings.ship_speed
        elif keys[pygame.K_w] and self.rect.top >= self.screen_rect.top:
            self.y -= 1 * self.settings.ship_speed
        elif keys[pygame.K_s] and self.rect.bottom <= self.screen_rect.bottom:
            self.y += 1 * self.settings.ship_speed

    def _update_vertical(self, keys):
        if keys[pygame.K_w] and self.ship_rect.top >= self.screen_rect.top:
            self.y -= 1 * self.settings.ship_speed
        elif keys[pygame.K_s] and self.ship_rect.bottom <= self.screen_rect.bottom:
            self.y += 1 * self.settings.ship_speed

    def draw_ship(self):
        self._check_invisibility_time()  # Blinking is a part of ship drawing, so I put it here.
        if self.god_mode:
            self._blink_ship()
        self.screen.blit(self.image, self.ship_rect)
        self.screen.blit(self.hit_box_surface, self.hit_box)
        self.screen.blit(self.core, self.rect)

    def _blink_ship(self):
        """To denote that the ship is invincible after respawning"""
        # Decrease then increase transparency
        if self.frame_timer == self.settings.FPS // 4:
            self.frame_timer = 0
            self.up = not self.up   # Reverse boolean. Ship will go transparent first anyway

        if self.up:
            self.alpha += self.alpha_modifier
        else:
            self.alpha -= self.alpha_modifier
        self.image.set_alpha(self.alpha)
        self.frame_timer += 1

    def _check_invisibility_time(self):
        now = pygame.time.get_ticks()
        # I think the god_mode bug is in here... I think I didn't put the start_respawn_timer here
        if now - self.start_respawn_time >= self.god_time:
            self.god_mode = False
            self.frame_timer = 0
            self.up = False
            self.alpha = 255
            self.image.set_alpha(255)  # Put the ship into opaque mode, now.

    def respawn_ship(self):
        """When ship is hit, respawn it at the midbottom of the screen.
        In the future, will give invisbility_time. Maybe do some blinking as well."""
        self.ship_rect.midbottom = self.screen_rect.midbottom
        self.rect.centerx = self.ship_rect.centerx
        self.rect.y = self.ship_rect.y + 5
        self.x = float(self.ship_rect.x)
        self.y = float(self.ship_rect.y)
        self.hit_box.center = self.rect.center

    def _fire_bullet(self):
        if len(self.main_game.bullets) < math.floor(self.settings.boolet_limit):
            bullet = Bullet(self.main_game)
            self.main_game.bullets.add(bullet)

    def _shoot_update(self, keys):
        self._check_bullet_cooldown()
        if keys[pygame.K_RETURN] and not self.shoot_disabled:
            self._fire_bullet()
            self.shoot_disabled = True

    def _check_bullet_cooldown(self):
        """Yeah, I don't want it to turn into a lazer beam of ultimate lethality"""
        time_now = pygame.time.get_ticks()
        if time_now - self.last_bullet_fired >= self.bullet_cooldown:
            self.shoot_disabled = False
            self.last_bullet_fired = pygame.time.get_ticks()

