import pygame
import json
from ship import Ship


class Scoreboard:
    """Display level, ship_left, high-score, and current score"""
    def __init__(self, main_game):
        self.main_game = main_game
        self.settings = self.main_game.settings
        self.stats = self.main_game.stats
        self.screen = main_game.screen
        self.screen_rect = self.main_game.screen_rect

        # Info font
        self.text_color = (235, 236, 240)
        self.font = pygame.font.Font("font/TravelingTypewriter.ttf", 30)
        self.hs_font = pygame.font.Font("font/TravelingTypewriter.ttf", 20)

        self.update_score()
        self.update_high_score()
        self.update_ships()
        self.update_level()

        self.scoreboard_height = self.high_score_rect.bottom

        # Invisibility settings
        self.alpha = 255  # 255: opaque, 0: transparent
        self.frame_timer = 0  # For decreasing and increasing alpha
        self.alpha_modifier = 255 // (self.settings.FPS // 10)
        self.up = False  # Boolean to detect whether to increase opacity or not

    def update_score(self):
        rounded = round(self.stats.score)
        score_formatted = f"{rounded:,}"
        self.score_display = self.font.render(score_formatted, True, self.text_color, None)

        # Display the score in the midtop of the screen
        self.score_rect = self.score_display.get_rect()
        self.score_rect.midtop = self.screen_rect.midtop

    def update_high_score(self):
        rounded = round(self.stats.high_score)
        score_formatted = f"High score: {rounded:,}"
        self.high_score_display = self.hs_font.render(score_formatted, True, self.text_color, None)

        # Display the score in the left of the screen
        self.high_score_rect = self.score_display.get_rect()
        self.high_score_rect.left = self.screen_rect.left
        self.high_score_rect.top = 50

    def update_ships(self):
        """Show how many ship' lives"""
        self.ships = pygame.sprite.Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.main_game)
            ship.rect.x = 5 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def update_level(self):
        """Update the current level"""
        level_str = f"Level:  {self.stats.level}"
        self.level_display = self.hs_font.render(level_str, True, self.text_color, None)
        # Display the level below the high score
        self.level_rect = self.level_display.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = 20

    def display_info(self):
        if self.main_game.ship.y <= self.scoreboard_height:
            self._transparent_scoreboard()
        else:
            self._opaque_scoreboard()
        self.screen.blit(self.score_display, self.score_rect)
        self.screen.blit(self.high_score_display, self.high_score_rect)
        self.screen.blit(self.level_display, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Check to see if there is a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.update_high_score()

    def save_high_score(self):
        """Save high score to a JSON file"""
        filepath = "high_score.json"
        with open(filepath, mode="w") as f:
            json.dump(self.stats.high_score, f)

    def load_high_score(self):
        """Load high score from a JSON file"""
        filepath = "high_score.json"
        try:
            with open(filepath, mode="r") as f:
                self.stats.high_score = json.load(f)
                self.update_high_score()
        except FileNotFoundError:
            return

    def _transparent_scoreboard(self):
        if self.frame_timer == self.settings.FPS // 4:
            self.frame_timer = 0
            self.up = not self.up

        if self.up:
            self.alpha -= self.alpha_modifier
            if self.alpha < 0:
                self.alpha = 0
        self._set_alpha()
        self.frame_timer += 1

    def _opaque_scoreboard(self):
        if self.frame_timer == self.settings.FPS // 4:
            self.frame_timer = 0
            self.up = not self.up   # Reverse boolean. Ship will go transparent first anyway

        if not self.up:
            self.alpha += self.alpha_modifier
            if self.alpha > 255:
                self.alpha = 255
        self._set_alpha()
        self.frame_timer += 1

    def _set_alpha(self):
        self.score_display.set_alpha(self.alpha)
        self.high_score_display.set_alpha(self.alpha)
        self.level_display.set_alpha(self.alpha)
        for ship in self.ships:
            ship.image.set_alpha(self.alpha)