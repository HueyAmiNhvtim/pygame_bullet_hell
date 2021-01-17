import pygame
from pygame.sprite import Group
import sys

# Maybe increase number of boolets to shoot per level. In the far future...
from settings import Settings
from ship import Ship
from bullet_ship import Bullet
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

        # Testing
        self.caption = "Wat"
        pygame.display.set_caption(self.caption)

        # Load resources
        self.ship_bullet = pygame.image.load("images/bullet_ship.bmp")

    def run_game(self):
        """Running the main loop of the game"""
        while True:
            self._check_events()
            self._display_fps()
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
            self._check_ship_hit_mask(alien_hit)  # False Warning

    def _check_ship_hit_mask(self, object_hit):
        """Check if ship actually hits using masks"""
        # Offset's there to check for the compared's mask's relative position with the calling mask.
        # In a mask collision, the calling's mask's origin is at (0,0), hence the need to transform the
        # coordinates of the called mask into a relative one, which will then push away the alien's mask so as to
        # get a more accurate rect detection
        # If offset is (0, 0), the mask collide is going to act
        # exactly like a rect collide.
        # Create mask after rect detection to save run time.... Mask is expensive time-wise...
        offset_x, offset_y = (object_hit.rect.left - self.ship.rect.left, object_hit.rect.top - self.ship.rect.top)
        actual_overlap = self.ship.mask.overlap(object_hit.mask, (offset_x, offset_y))
        if actual_overlap:
            # print("Collision detected!")
            self.ship.respawn_ship()  # Maybe not doing mask with the alien and the ship.

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
        alien.create_destination_and_vector()
        self.aliens.add(alien)

    def _update_aliens(self):
        """Update alien_positions and draw them out..."""
        self.aliens.update()
        for alien in self.aliens:
            if alien.rect.y < 0 or alien.rect.y > self.settings.screen_height or alien.rect.x < 0 or alien.rect.x > self.settings.screen_width:
                sys.exit()
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
            self.bullets.empty()

    def _display_fps(self):
        """Show the program's FPS in the window handle.WILL DELETE LATER.
        THANKS MEKIRE!"""
        caption = f"{self.caption} - FPS: {clock.get_fps():.2f}"
        pygame.display.set_caption(caption)


if __name__ == "__main__":
    game = WhatIsThisAbomination()
    game.run_game()
