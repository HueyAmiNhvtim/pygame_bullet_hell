import pygame
from pygame.sprite import Group
import sys
import math

# Maybe increase number of boolets to shoot per level. In the far future... DONE!
from settings import Settings
from ship import Ship
from bullet_ship import Bullet
from alien import Alien
from stats import Stats
from button import Button
from scoreboard import Scoreboard


# TO-DO: ship_hit in around line 87, uhm, should delete walrus one lest I want to use mask
#        Summon aliens on both side of the screen. SYMMETRY FTW. ABANDONED!
#        Make the aliens move on the screen using vectors.  DONE!
#        With vectors maybe I can do what I want, provided I don't procrastinate
#        by playing Spanish Dark Souls. AHHHHHHHHHHHHH
# TO-DO:
#       Make the ship blink faster... nah,
#       ship will be invincible to the boolets. DONE!
#       Event queue for each aliens. Basically consist of events. Use deque for this, I guess. Use burst-left as
#       indicator for a need to move onto another pattern. DONE!
#       Make moar patterns.... The tri non-homing one, the 360 no scope one, and then, the, uhm... 5 PATTERNS ALREADY
# To be frank though, I'm kinda worried about my project...
clock = pygame.time.Clock()


class WhatIsThisAbomination:
    def __init__(self):
        """LOAD GAME RESOURCES AND MANAGE GAME RESOURCES"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        self.ship = Ship(self)
        self.stats = Stats(self)
        self.scoreboard = Scoreboard(self)
        self.scoreboard.load_high_score()

        # Groups.
        self.bullets = Group()
        self.aliens = Group()
        self.bombs = Group()
        self.alien_bullets = Group()  # To account for bullets fired by the aliens

        # Background colors. Hopefully will be replaced by animated frame I rip off from the Internet
        # oh god. the vectors. aaaaaaaaaaaaaaaa
        self.screen.fill(self.settings.bg_color)

        # Create aliens
        self._create_aliens()

        # Caption and play button
        self.caption = "My 'game'"
        pygame.display.set_caption(self.caption)
        self.instructions_title = Button(self, "INSTRUCTIONS", -2, font_size=24, bar_height=30)
        self.instructions = Button(self, "WASD to move;\nSpace to shoot;\nShift to slow down", -1, font_size=24,
                                   bar_height=30, bar_width=700)
        self.play_button = Button(self, "Play (P)", 0)
        self.escape_button = Button(self, "Esc?", 1)

        # Load resources. I can't justify myself putting in the SpriteSheet code from
        # the Net and given my time constraint, I have to do this ugly. Extremely ugly
        self.ship_bullet = pygame.image.load("images/bullet_ship.bmp")
        # self.bomb_ship = pygame.image.load("images/bomb_effect.bmp")  I don't have enough time to learn how to rotate and expand image from center
        self.al_bullet_one = pygame.image.load("images/bullet_al.bmp")
        self.al_bullet_two = pygame.image.load("images/bullet_al_2.bmp")
        self.al_bullet_three = pygame.image.load("images/bullet_al_3.bmp")
        self.al_bullet_four = pygame.image.load("images/bullet_al_4.bmp")
        self.al_bullet_five = pygame.image.load("images/bullet_al_5.bmp")

    def run_game(self):
        """Running the main loop of the game"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_objects()
            self._update_screen()
            clock.tick(self.settings.FPS)

    def _check_events(self):
        """Check for key presses for menu navigation."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.scoreboard.save_high_score()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self._draw_bullets()
        self.ship.draw_ship()
        if self.stats.game_active:
            for alien in self.aliens:
                alien.update_health()
                alien.draw_bar_health()
        else:
            self.instructions_title.draw_button()
            self.instructions.draw_button()
            self.play_button.draw_button()
            self.escape_button.draw_button()
        self.aliens.draw(self.screen)
        self.scoreboard.display_info()
        self._draw_alien_bullets()
        pygame.display.flip()

    def _update_objects(self):
        """Update all object's movements"""
        self._update_ships()
        self._update_aliens()
        self._update_bullets()
        self._update_alien_bullets()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets:
            if bullet.rect.y < 0:
                self.bullets.remove(bullet)

    def _update_alien_bullets(self):
        self.alien_bullets.update()
        for bullet in self.alien_bullets:
            if bullet.rect.y < 0 or bullet.rect.y > self.screen_rect.height:
                self.alien_bullets.remove(bullet)
            elif bullet.rect.x < 0 or bullet.rect.x > self.screen_rect.width:
                self.alien_bullets.remove(bullet)

    def _draw_bullets(self):
        for bullet in self.bullets:
            bullet.draw_bullet()  # False warning. Plz ignore.

    def _draw_alien_bullets(self):
        for bullet in self.alien_bullets:
            bullet.draw_bullet()  # False warning. Plz ignore

    def _update_ships(self):
        self._check_ship_hit()

    def _check_ship_hit(self):
        """Check if ship hits aliens and/ or their bullets"""
        if not self.ship.god_mode:
            if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
                bullet_hit = pygame.sprite.spritecollideany(self.ship, self.alien_bullets)
                self._check_ship_hit_mask(bullet_hit)   # False warning
            elif pygame.sprite.spritecollideany(self.ship, self.aliens):
                alien_hit = pygame.sprite.spritecollideany(self.ship, self.aliens)
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
        collision = self.ship.hit_box.colliderect(object_hit.actual_rect)
        if object_hit not in self.aliens:
            if actual_overlap and not self.ship.god_mode:
                # If the ship's core is in the mask with of the bullet, add score per FRAME.
                # Similar to Touhou's grazing mechanics.
                self.stats.score += self.settings.graze_increment
                self.scoreboard.update_score()
                self.scoreboard.check_high_score()
            if collision:
                self._ship_dead_consequence()
        else:
            if collision and not self.ship.god_mode:
                self.stats.score += self.settings.graze_increment
                self.scoreboard.update_score()
                self.scoreboard.check_high_score()
            if actual_overlap:
                self._ship_dead_consequence()
        self._check_ship_conditions()

    def _ship_dead_consequence(self):
        # Respawn ship and then set a marker to act for invincible cooldown period.
        # print("Collision detected!")
        self.ship.respawn_ship()  # Maybe not doing mask with the alien and the ship.
        self.ship.start_respawn_time = pygame.time.get_ticks()
        self.stats.ships_left -= 1
        self.scoreboard.ships.remove(list(self.scoreboard.ships)[-1])
        self.ship.god_mode = True

    def _check_keydown_events(self, event):
        """Respond to key presses appropriately"""
        if event.key == pygame.K_ESCAPE:
            self.scoreboard.save_high_score()
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_LSHIFT:
            # Slow down ship by a constant rate if LSHIFT is pressed
            self.settings.ship_speed *= self.settings.slow_scale
        elif event.key == pygame.K_p:
            self.stats.game_active = True
            self._check_play_button()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_LSHIFT:
            # Restore ship speed if LSHIFT is not pressed anymore
            self.settings.ship_speed *= 1 / self.settings.slow_scale

    def _create_aliens(self):
        """Create row of aliens on the first row. In the future, might change"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.screen_rect.width - 3 * alien_width
        # max_alien_per_row = available_space_x // (alien_width + alien_width // 5)
        # for j in range(2):
            # for i in range(max_alien_per_row):
                # self._create_alien(i)

        for i in range(int(round(self.settings.aliens_on_screen))):
            self._create_alien(i)

    def _create_alien(self, column_number, row_number=0):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width // 5 + (alien_width + alien_width // 5) * column_number
        alien.y = alien.rect.height + (alien_height + alien_height // 5) * row_number
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        alien.create_destination_and_vector()
        self.aliens.add(alien)

    def _update_aliens(self):
        """Update alien_positions and draw them out..."""
        self.aliens.update()
        self._check_alien_bullet_collisions()

    def _check_alien_bullet_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, False)
        if collisions:
            for alien in list(collisions.values())[0]:  # False warning
                # Minus health everytime alien is hit, which the reason why there is
                # the boolean False as the parameters for the aliens.
                alien.health -= 1
                if alien.health == 0:
                    self.aliens.remove(alien)
                    self.stats.score += self.settings.alien_points
                    self.scoreboard.update_score()
                    self.scoreboard.check_high_score()
        self._end_alien_lost()

    def _end_alien_lost(self):
        if len(self.aliens) == 0:
            # Create new group. In the future, this is where enemies will gain new patterns
            # and gain more strength in number. Provided I don't procrastinate by
            # playing Spanish Dark Souls, again.
            self._create_aliens()
            self.ship.respawn_ship()
            self.bullets.empty()
            self.bombs.empty()
            self.stats.level += 1
            if self.stats.level % 3 == 0:
                self.stats.ships_left += 1
            self.settings.increase_level()
            self.scoreboard.update_level()
            self.scoreboard.update_ships()
            self.alien_bullets.empty()

    def _check_ship_conditions(self):
        """If health is empty, reset the current stats"""
        if self.stats.ships_left == 0:
            self.stats.game_active = False
            self.stats.reset_stats()
            self.scoreboard.update_ships()
            self.scoreboard.update_score()
            self.scoreboard.update_level()
            self.settings.initialize_dynamic_settings()

            # Change play button slightly
            self.play_button.message = "Play again? (P to play)"
            self.play_button.update_msg()
            self.play_button.insert_msg()

            self.scoreboard.display_info()
            pygame.mouse.set_visible(True)

    def _check_play_button(self):
        """Start a new game"""
        # Reset game statistics
        self.stats.reset_stats()
        self.stats.game_active = True

        # Hide mouse buttons
        pygame.mouse.set_visible(False)

        # Get rid of any remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()

        # Create a new fleet and center ship
        self._create_aliens()
        self.ship.respawn_ship()

        # Reset the game settings
        self.settings.initialize_dynamic_settings()
        self.ship.god_mode = False
        self.ship.image.set_alpha(255)


if __name__ == "__main__":
    game = WhatIsThisAbomination()
    game.run_game()
