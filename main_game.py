import pygame
from pygame.sprite import Group
import sys

# Maybe increase number of boolets to shoot per level. In the far future...
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


clock = pygame.time.Clock()


class WhatIsThisAbomination:
    def __init__(self):
        """LOAD GAME RESOURCES AND MANAGE GAME RESOURCES0"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.ship = Ship(self)

        # Groups.
        self.bullets = Group()
        self.aliens = Group()

        # Background colors. Hopefully will be replaced by animated frame I rip off from the Internet
        # oh god. the vectors. aaaaaaaaaaaaaaaa
        self.screen.fill(self.settings.bg_color)

    def run_game(self):
        """Running the main loop of the game"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()
            clock.tick(60)

    def _check_events(self):
        """Check for key presses for menu navigation."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self._update_bullets()
        self.ship.draw_ship()
        self._draw_bullets()
        pygame.display.flip()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.boolet_limit:
            bullet = Bullet(self)
            self.bullets.add(bullet)

    def _update_bullets(self):
        for bullet in self.bullets:
            if bullet.rect.y < 0:
                self.bullets.remove(bullet)
        print(len(self.bullets))

    def _draw_bullets(self):
        self.bullets.update()
        for bullet in self.bullets:
            bullet.draw_bullet()  # False warning. Plz ignore.

    def _check_keydown_events(self, event):
        """Respond to key presses appropriately"""
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_RETURN:
            self._fire_bullet()
        elif event.key == pygame.K_LSHIFT:
            # Slow down ship by a constant rate if LSHIFT is pressed
            self.settings.ship_speed *= self.settings.slow_scale

    def _check_keyup_events(self, event):
        if event.key == pygame.K_LSHIFT:
            # Restore ship speed if LSHIFT is not pressed anymore
            self.settings.ship_speed *= 1 / self.settings.slow_scale\

    def _create_aliens(self):
        """Create two aliens on the first row. In the future, might change"""
        pass


if __name__ == "__main__":
    game = WhatIsThisAbomination()
    game.run_game()
