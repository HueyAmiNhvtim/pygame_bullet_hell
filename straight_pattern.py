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
        self.burst_disabled = False  # This for delay between burst
        self.shoot_disabled = False  # This is for boolet's delay
        self.burst_cooldown = self.settings.burst_cooldown
        self.bullet_cooldown = self.settings.ali_bullet_cooldown
        self.last_time = pygame.time.get_ticks()

    def shoot_burst(self):
        """Shoot the boolet in burst of straight line. Do it like the alien_movement cooldown"""
        bullet = BulletAlienUno(self.main_game)
        bullet.rect.midtop = self.shooter.rect.midbottom
        self.main_game.alien_bullets.add(bullet)

    def shoot_boolet(self):
        """Shoot each boolet. Do it like the alien_movement cooldown"""
        pass
