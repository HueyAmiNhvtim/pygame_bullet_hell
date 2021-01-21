import pygame
from bullet_patterns.aimed_pattern import AimedPattern
from bullet_patterns.tri_pattern import TriPattern
from bullet_patterns.no_scope import NoScope
from bullet_patterns.homing_pattern import HomingPattern
from bullet_patterns.cyclone import Cyclone
from collections import deque
# TO-DO: Line up the event order, as in like the target will only activate movement's countdown
# after finishing a pattern. The pattern manager should be responsible for choosing the patterns from now on.
# Also, fix the tri-pattern bullet
# Yeah, the deque can be improved...


class PatternManager:
    """A class for maintaining the alien's choice of bullet patterns"""
    def __init__(self, main_game, shooter):
        self.shooter = shooter
        self.pattern_cooldown = main_game.settings.pattern_cooldown
        self.first_pattern = AimedPattern(main_game, self.shooter)
        self.second_pattern = TriPattern(main_game, self.shooter)
        self.third_pattern = NoScope(main_game, self.shooter)
        self.fourth_pattern = HomingPattern(main_game, self.shooter)
        self.fifth_pattern = Cyclone(main_game, self.shooter)
        # self.event_deque = deque([self.first_pattern, self.fifth_pattern])
        self.event_deque = deque(
            [self.first_pattern, self.second_pattern, self.first_pattern, self.third_pattern, self.first_pattern,
             self.fourth_pattern, self.first_pattern, self.fifth_pattern])
        self.wait = False
        self.last_switch = pygame.time.get_ticks()

    def use_pattern(self):
        self._check_pattern_cooldown()
        if not self.wait:
            self.event_deque[0].shoot_burst()
            self.wait = True

    def switch_pattern(self):
        """Event queue using queue"""
        event = self.event_deque.popleft()
        event.reset()
        self.event_deque.append(event)
        self.last_switch = pygame.time.get_ticks()

    def _check_pattern_cooldown(self):
        now = pygame.time.get_ticks()
        if now - self.last_switch >= self.pattern_cooldown:
            self.wait = False


