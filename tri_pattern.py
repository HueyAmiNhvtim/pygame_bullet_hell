import pygame
from bullet_alien import BulletAlienDos


class TriPattern:
    """A pattern class for shooting boolets in a straightline of 3"""
    def __init__(self, main_game, shooter):
        self.main_game = main_game
        self.screen = main_game.screen
        self.settings = main_game.settings
        self.shooter = shooter

        # Flags to use in tandem with cooldown
        self.burst_disabled = False  # This for delay between burst
        self.shoot_disabled = False  # This is for boolet's delay

        # Imported from settings.py
        self.burst_cooldown = self.settings.tri_burst_cooldown
        self.bullet_cooldown = self.settings.tri_bullet_cooldown
        self.bullets_per_burst = self.settings.tri_bullets_per_burst
        self.last_burst_fired = pygame.time.get_ticks()
        self.last_bullet_fired = pygame.time.get_ticks()
        self.angle = self.settings.angle_between_stream

        # Dynamic bullet_count and burst_count
        self.bullets_left = self.bullets_per_burst

    def shoot_burst(self):
        """Shoot the boolet in burst of straight line. Do it like the alien_movement cooldown"""
        self._check_burst_cooldown()
        """yeah, I have to check if any bursts left to move onto next pattern"""
        if not self.burst_disabled:
            """check if any bullets left. Otherwise, reduce burst count and then do a new burst"""
            if self.bullets_left != 0:
                # Check to see whether the burst is finished
                self._check_bullet_cooldown()
                if not self.shoot_disabled:
                    # Shoot a bullet and then disable the shooting ability until cooldown
                    self.shoot_boolet()
                    self.last_bullet_fired = pygame.time.get_ticks()
                    self.bullets_left -= 1
                    self.shoot_disabled = True
            else:
                # If burst is finished reset burst and recorded last burst_time.
                self.bullets_left = self.bullets_per_burst
                self.last_burst_fired = pygame.time.get_ticks()
                self.burst_disabled = True

    def shoot_boolet(self):
        """Shoot each triplet of bullets"""
        angle = self.angle
        for i in range(3):
            bullet = BulletAlienDos(self.main_game, shooter=self.shooter)
            bullet.vector[0] = 0
            bullet.vector[1] = 1
            bullet.normalized_vector = bullet.vector.normalize()
            bullet.normalized_vector = bullet.normalized_vector.rotate(angle)
            angle -= self.angle
            self.main_game.alien_bullets.add(bullet)

    def _check_burst_cooldown(self):
        time_now = pygame.time.get_ticks()
        # I think I might have to put in the number of bullets_left in a burst.
        if time_now - self.last_burst_fired >= self.burst_cooldown:
            self.burst_disabled = False

    def _check_bullet_cooldown(self):
        """Yeah, I don't want it to turn into a lazer beam of ultimate lethality"""
        time_now = pygame.time.get_ticks()
        if time_now - self.last_bullet_fired >= self.bullet_cooldown:
            self.shoot_disabled = False

    def reset(self):
        # Flags to use in tandem with cooldown
        self.burst_disabled = False  # This for delay between burst
        self.shoot_disabled = False  # This is for boolet's delay

        # Imported from settings.py
        self.burst_cooldown = self.settings.tri_burst_cooldown
        self.bullet_cooldown = self.settings.tri_bullet_cooldown
        self.bullets_per_burst = self.settings.tri_bullets_per_burst
        self.last_burst_fired = pygame.time.get_ticks()
        self.last_bullet_fired = pygame.time.get_ticks()

        # Dynamic bullet_count and burst_count
        self.bullets_left = self.bullets_per_burst
