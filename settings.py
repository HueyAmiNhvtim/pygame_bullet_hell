class Settings:
    """Store all settings for the main file"""
    def __init__(self):
        """Initialize game settings"""
        self.screen_width = 1050
        self.screen_height = 700
        self.bg_color = (49, 0, 71)

        # Ship settings
        self.slow_scale = 1 / 3
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # For settings that can be changed during the game.
        # Ship settings
        self.ship_speed = 5
