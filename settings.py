# ALL COOLDOWNS ARE MEASURED IN MILLISECONDS UNLESS EXPLICITLY TOLD OTHERWISE!


class Settings:
    """Store all settings for the main file"""
    def __init__(self):
        """Initialize game settings"""
        self.screen_width = 1050
        self.screen_height = 700
        self.bg_color = (49, 0, 71)
        self.FPS = 60

        # Ship settings
        self.slow_scale = 1 / 4
        self.god_time = 3000
        self.circle_color = (105, 105, 105)

        # Alien settings:
        self.movement_cooldown = 5000

        # Bullet - ship settings.
        self.bullet_speed = 7
        self.bullet_height = 15
        self.bullet_width = 5
        self.bullet_color = (0, 255, 0)
        self.boolet_limit = 4

        # Pattern settings
        self.ali_bullet_speed = 1
        self.pattern_cooldown = 5000  # Cool down between patterns

        # Bullet - alien settings
        # How many bullets allowed in a burst. Expect to have a lot of these settings for different patterns
        self.homing_bullets_per_burst = 5
        self.homing_bullet_cooldown = 100
        self.homing_burst_cooldown = 400   # Cooldown between burst

        # Tri-Pattern
        self.tri_bullets_per_burst = 4
        self.tri_cooldown = 300
        self.tri_bullet_cooldown = 500
        self.tri_burst_cooldown = 800
        self.angle_between_stream = 30  # Use this to rotate the vector for each stream
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # For settings that can be changed during the game.
        # Ship settings
        self.ship_speed = 5

        # Alien settings
        self.alien_speed = 4
        self.alien_health = 3
