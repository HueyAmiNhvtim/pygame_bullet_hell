import pygame
from pygame.sprite import Group
import sys
import random as rdn

# Maybe increase number of boolets to shoot per level. In the far future...
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

# TO-DO: ship_hit in around line 87, uhm, should delete walrus one lest I want to use mask
#        Summon aliens on both side of the screen. SYMMETRY FTW
#        Make the aliens move on the screen using vectors.
#        With vectors maybe I can do what I want, provided I don't procrastinate
#        by playing Spanish Dark Souls. AHHHHHHHHHHHHH
# To be frank though, I'm kinda worried about my project...
clock = pygame.time.Clock()


class WhatIsThisAbomination:
    def __init__(self):
        """LOAD GAME RESOURCES AND MANAGE GAME RESOURCES0"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        self.ship = Ship(self)

        # Groups.
        self.bullets = Group()
        self.aliens = Group()
        self.alien_bullet = Group()  # To account for bullets fired by the aliens

        # Background colors. Hopefully will be replaced by animated frame I rip off from the Internet
        # oh god. the vectors. aaaaaaaaaaaaaaaa
        self.screen.fill(self.settings.bg_color)

        # Create aliens
        self._create_aliens()

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
        self._update_ships()
        self._update_aliens()
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
        # print(len(self.bullets))

    def _draw_bullets(self):
        self.bullets.update()
        for bullet in self.bullets:
            bullet.draw_bullet()  # False warning. Plz ignore.

    def _update_ships(self):
        self._check_ship_hit()
        self.ship.draw_ship()

    def _check_ship_hit(self):
        """Check if ship hits aliens and/ or their bullets"""
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullet):
            self.ship.respawn_ship()
        elif alien_hit := pygame.sprite.spritecollideany(self.ship, self.aliens):

            self.ship.respawn_ship()  # Maybe not doing mask with the alien and the ship.
        pass

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
        """Create row of aliens on the first row. In the future, might change"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.screen_rect.width - 3 * alien_width
        max_alien_per_row = available_space_x // (alien_width + alien_width // 5)
        for i in range(max_alien_per_row):
            self._create_alien(i)

    def _create_alien(self, column_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width // 5 + (alien_width + alien_width // 5) * column_number
        alien.rect.x = alien.x
        self.aliens.add(alien)

    def _update_aliens(self):
        """Update alien_positions and draw them out..."""
        self.aliens.draw(self.screen)
        self._check_alien_bullet_collisions()

    def _check_alien_bullet_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, False)
        if collisions:
            for alien in list(collisions.values())[0]:  # False warning
                # Minus health everytime alien is hit, which the reason why there is
                # the boolean False as the parameters
                alien.health -= 1
                if alien.health == 0:
                    self.aliens.remove(alien)

        if len(self.aliens) == 0:
            # Create new group. In the future, this is where enemies will gain new patterns
            # and gain more strength in number. Provided I don't procrastinate by
            # playing Spanish Dark Souls, again.
            self._create_aliens()
            self.ship.respawn_ship()


if __name__ == "__main__":
    game = WhatIsThisAbomination()
    game.run_game()
