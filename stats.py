class Stats:
    """Tracking stats from the player"""
    def __init__(self, main_game):
        self.settings = main_game.settings

        self.game_active = True  # Flag for the Play button...

        # General ship_stats:
        self.ships_left = self.settings.ships_health
        self.score = 0
        self.level = 1

        # MUST NEVER BE RESET...
        self.high_score = 0

    def reset_stats(self):
        """Reset stats after each game"""
        self.ships_left = self.settings.ships_health
        self.score = 0
        self.level = 1

