import pygame
import sys

from settings import Settings
from ship import Ship


clock = pygame.time.Clock()


class WhatIsThisAbomination:
    def __init__(self):
        """LOAD GAME RESOURCES AND MANAGE GAME RESOURCES0"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.ship = Ship(self)

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

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.draw_ship()
        pygame.display.flip()

    def _check_keydown_events(self, event):
        """Respond to key presses appropriately"""
        if event.key == pygame.K_q:
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    game = WhatIsThisAbomination()
    game.run_game()
