import pygame
from bullet_alien import BulletAlienUno

# TO-DO:
# Event queue for each aliens. Basically consist of events. Use deque for this, I guess.


class StraightPattern:
    """A pattern class for shooting boolets in a straightline"""
    def __init__(self, alien, main_game):
        self.main_game = main_game
        self.screen = main_game.screen
        self.settings = main_game.settings
        self.shooter = alien

        # Flags to use in tandem with cooldown
        self.burst_disabled = False  # This for delay between burst
        self.shoot_disabled = False  # This is for boolet's delay

        # Imported from settings.py
        self.burst_cooldown = self.settings.burst_cooldown
        self.bullet_cooldown = self.settings.ali_bullet_cooldown
        self.burst_num = self.settings.burst_num
        self.bullets_per_burst = self.settings.ali_burst_straight
        self.last_burst_time = pygame.time.get_ticks()
        self.last_bullet_fired = pygame.time.get_ticks()

        # Dynamic bullet_count and burst_count
        self.num_bullets_left = self.bullets_per_burst
        self.num_burst_left = self.burst_num

    def shoot_burst(self):
        """Shoot the boolet in burst of straight line. Do it like the alien_movement cooldown"""
        self._check_burst_cooldown()
        """yeah, I have to check if any bursts left to move onto next pattern"""
        if not self.burst_disabled:
            """check if any bullets left. Otherwise, reduce burst count and then do a new burst"""
            pass
        pass

    def shoot_boolet(self):
        """Shoot each boolet. Do it like the alien_movement cooldown"""
        bullet = BulletAlienUno(self.main_game)
        bullet.rect.midtop = self.shooter.rect.midbottom
        bullet.vector[0], bullet.vector[1] = 0, 1  # Set the vector to shoot straight down
        self.main_game.alien_bullets.add(bullet)
        pass

    def _check_burst_cooldown(self):
        time_now = pygame.time.get_ticks()
        # I think I might have to put in the number of bullets_left in a burst.
        if time_now - self.last_burst_time >= self.burst_cooldown:
            self.burst_disabled = False
            # I think that I might have to reduce the number of burst here...

    def _check_bullet_cooldown(self):
        """Yeah, I don't want it to turn into a lazer beam of ultimate lethality"""
        time_now = pygame.time.get_ticks()
        if time_now - self.last_bullet_fired >= self.bullet_cooldown:
            self.shoot_disabled = False
        pass