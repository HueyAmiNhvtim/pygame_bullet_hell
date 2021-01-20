import pygame
import numpy
from pygame.sprite import Sprite
from pygame import Vector2
# TO-DO: Rotate sprite, too in bulletAlienQuattro. Use prev vector with new vector and then calculate the angle
#        use pygame.transform.rotate(image, angle) to rotate it. Also update the surface mask, too.
#        Have the limited tracking time
#        Fix update_vector


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

        # Start each bullet out of the alien. This is where the alien will shoot bullet.
        self.rect = self.image.get_rect()
        self.rect.midtop = shooter.rect.midbottom
        self.bullet_rect.center = self.rect.center
        self.angle = 0
        # speed
        self.speed = self.settings.ali_bullet_speed
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
        self.x += self.normalized_vector[0] * self.speed
        self.y += self.normalized_vector[1] * self.speed
        self.rect.x = self.x
        self.rect.y = self.y
        self.bullet_rect.center = self.rect.center


class BulletAlienDos(BulletAlienUno):
    """Exactly same class, just with different image"""
    def __init__(self, main_game, shooter):
        super().__init__(main_game, shooter)
        self.image = main_game.al_bullet_two
        self.speed = self.speed * 1.5


class BulletAlienTres(BulletAlienUno):
    """Exactly same class, just with different image"""
    def __init__(self, main_game, shooter):
        super().__init__(main_game, shooter)
        self.image = main_game.al_bullet_three
        self.rect.center = shooter.rect.center
        self.bullet_rect.center = self.rect.center


class BulletAlienQuattro(BulletAlienUno):
    """Inherit a bit, but this time, it's gonna be homing bullets"""
    def __init__(self, main_game, shooter):
        super().__init__(main_game, shooter)
        self.image = main_game.al_bullet_four
        self.speed = self.speed * 5
        self.bullet_hitbox = pygame.Surface(size=(4, 4))  # True hitbox of bullet for some sick bullet dodging
        self.bullet_rect = self.bullet_hitbox.get_rect()
        self.mask = pygame.mask.from_surface(self.bullet_hitbox)
        self.main_game = main_game  # Hopefully this won't slow down the game

        # Homing purpose
        self.update_cooldown = main_game.settings.homing_update_tick  # I don't know if that's the right word to use
        self.homing_time = main_game.settings.homing_time
        self.core_x = 0  # Coordinate of core for homing purpose
        self.core_y = 0

        self.new_vector = Vector2()
        self.last_time = pygame.time.get_ticks()
        self.homing_start = pygame.time.get_ticks()  # Start right at the bullet's creation
        # Flag
        self.homing = True

    def update(self):
        """Check for update tick in order to head for the ship"""
        self._check_for_homing_time()
        self._check_for_vector_update()
        self.x += self.normalized_vector[0] * self.speed
        self.y += self.normalized_vector[1] * self.speed
        self.rect.x = self.x
        self.rect.y = self.y
        self.bullet_rect.center = self.rect.center

    def _check_for_vector_update(self):
        if self.homing:
            now = pygame.time.get_ticks()
            if now - self.last_time >= self.update_cooldown:
                self._change_vector()
                self.last_time = pygame.time.get_ticks()

    def _check_for_homing_time(self):
        """Check if homing duration for the bullet is """
        now = pygame.time.get_ticks()
        if now - self.homing_start >= self.homing_time:
            self.homing = False

    def _change_vector(self):
        self.new_vector[0] = self.main_game.ship.rect.x - self.rect.x
        self.new_vector[1] = self.main_game.ship.rect.y - self.rect.y  # Set the vector to aim at the ship's position
        if self.new_vector.length() != 0 and not self.main_game.ship.god_mode:
            self.normalized_vector = self.new_vector.normalize()
            self.vector[0], self.vector[1] = self.new_vector[0], self.new_vector[1]
            self.last_time = pygame.time.get_ticks()  # Record the last time bullet change vectors.

