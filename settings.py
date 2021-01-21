# ALL COOLDOWNS ARE MEASURED IN MILLISECONDS UNLESS EXPLICITLY TOLD OTHERWISE!
# Maybe put the event queue there so every 2 levels add a new pattern to the aliens


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
        self.circle_color = (105, 105, 105)  # I don't remember where I put this
        self.ships_health = 1000

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
        self.pattern_cooldown = 500  # Cool down between patterns
        # self.event_deque = deque([self.first_pattern, self.second_pattern, self.first_pattern, self.third_pattern, self.first_pattern,self.fourth_pattern])

        # Bullet - alien settings
        # How many bullets allowed in a burst. Expect to have a lot of these settings for different patterns
        self.aiming_bullets_per_burst = 2
        self.aiming_bullet_cooldown = 100
        self.aiming_burst_cooldown = 400   # Cooldown between burst

        # Tri-Pattern
        self.tri_bullets_per_burst = 4
        self.tri_cooldown = 300
        self.tri_bullet_cooldown = 500
        self.tri_burst_cooldown = 800
        self.angle_between_stream = 30  # Use this to rotate the vector for each stream

        # 360 no scope. noscope shortened into nope...
        self.nope_rings_per_burst = 3
        self.nope_cooldown = 300  # yeah, this cooldown between pattern is never used for some reason
        self.nope_bullet_cooldown = 500  # This becomes cooldown between rings. Might implement one between individual bullets later
        self.nope_burst_cooldown = 2000
        self.nope_bullets_ring = 10  # Number of bullets per ring.

        # homing_bullets
        self.homing_bullets_per_burst = 1
        self.homing_bullet_cooldown = 100
        self.homing_burst_cooldown = 1000  # Cooldown between burst
        self.homing_update_tick = 150  # Rate to update bullet's vector
        self.homing_time = 3000  # Total time bullets allowed to homing

        # Cooldown
        self.cyclone_bullet_cooldown = 25
        self.cyclone_time = 3000
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # For settings that can be changed during the game.
        # Ship settings
        self.ship_speed = 5

        # Alien settings
        self.alien_speed = 3
        self.alien_health = 3

    def increase_level(self):
        pass