import pygame

from bullet_patterns.no_scope import NoScope
from bullet_alien import BulletAlienCinco


class Cyclone(NoScope):
    """A derivative of the NoScope class"""
    def __init__(self, main_game, shooter):
        super().__init__(main_game, shooter)
        self.bullets_per_ring = self.settings.nope_bullets_ring * 2.5
        self.angle = 360 // self.bullets_per_ring

        self.bullet_cooldown = self.settings.cyclone_bullet_cooldown
        self.cyclone_time = self.settings.cyclone_time
        self.start_time = pygame.time.get_ticks()
        self.angle_increment = self.angle
        self.no_scope = NoScope(main_game, shooter)

        self.cyclone = True
        self.confirmed_start = True

    def shoot_burst(self):
        """Shoot the boolet in burst of straight line. Do it like the alien_movement cooldown"""
        self._check_cyclone_time()
        """yeah, I have to check if any bursts left to move onto next pattern"""
        if self.cyclone:
            self._check_bullet_cooldown()
            if not self.shoot_disabled:
                # Shoot a bullet and then disable the shooting ability until cooldown
                self.shoot_boolet()
                self.last_bullet_fired = pygame.time.get_ticks()
                self.bullets_left -= 1
                self.angle -= self.angle_increment
                self.shoot_disabled = True
        else:
            self.no_scope.shoot_burst()

    def shoot_boolet(self):
        """A cyclone of bullets"""
        bullet = BulletAlienCinco(self.main_game, shooter=self.shooter)
        bullet.vector[0] = 0
        bullet.vector[1] = 1
        bullet.normalized_vector = bullet.vector.normalize()
        bullet.normalized_vector = bullet.normalized_vector.rotate(self.angle)
        self.main_game.alien_bullets.add(bullet)

    def _check_bullet_cooldown(self):
        """Yeah, I don't want it to turn into a lazer beam of ultimate lethality"""
        now = pygame.time.get_ticks()
        if now - self.last_bullet_fired >= self.bullet_cooldown:
            self.shoot_disabled = False

    def _check_cyclone_time(self):
        now = pygame.time.get_ticks()
        if self.confirmed_start:
            self.start_time = pygame.time.get_ticks()
            self.confirmed_start = False
        if now - self.start_time >= self.cyclone_time:
            self.cyclone = False

    def reset(self):
        # Flags to use in tandem with cooldown
        self.cyclone = True  # This for delay between burst
        self.shoot_disabled = False  # This is for boolet's delay
        self.confirmed_start = True
        self.angle = 0

        # Imported from settings.py
        self.start_time = pygame.time.get_ticks()
        self.last_bullet_fired = pygame.time.get_ticks()

        # Dynamic bullet_count and burst_count
        self.bullets_left = self.bullets_per_burst