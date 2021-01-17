# TO-DO:


class Settings:
    """Store all settings for the main file"""
    def __init__(self):
        """Initialize game settings"""
        self.screen_width = 1050
        self.screen_height = 700
        self.bg_color = (49, 0, 71)

        # Ship settings
        self.slow_scale = 1 / 5

        # Alien settings:
        self.movement_cooldown = 3000

        # Bullet - ship settings.
        self.bullet_speed = 7
        self.bullet_height = 15
        self.bullet_width = 5
        self.bullet_color = (0, 255, 0)
        self.boolet_limit = 4

        # Bullet - alien settings
        self.ali_bullet_speed = 7
        self.ali_burst_straight = 6  # How many bullets allowed in a straight burst
        self.burst_num = 3  # How many times to repeat a pattern
        self.ali_bullet_cooldown = 300
        self.burst_cooldown = 500

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # For settings that can be changed during the game.
        # Ship settings
        self.ship_speed = 5

        # Alien settings
        self.alien_speed = 10
        self.alien_health = 3
