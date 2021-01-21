import pygame
import random
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
        self.settings = main_game.settings
        self.pattern_cooldown = self.settings.pattern_cooldown
        self.pattern_choice = int(round(self.settings.pattern_choice))  # how many patterns aliens are allowed to choose
        self.pattern_tier = int(round(self.settings.pattern_tier))

        self.first_pattern = AimedPattern(main_game, self.shooter)
        self.second_pattern = TriPattern(main_game, self.shooter)
        self.third_pattern = NoScope(main_game, self.shooter)
        self.fourth_pattern = HomingPattern(main_game, self.shooter)
        self.fifth_pattern = Cyclone(main_game, self.shooter)

        self.event_dictionary = {0: self.first_pattern, 1: self.second_pattern, 2: self.third_pattern,
                                 3: self.fourth_pattern, 4: self.fifth_pattern}

        self.event_deque = self._choose_pattern()
        self.wait = False
        self.last_switch = pygame.time.get_ticks()

    def _choose_pattern(self):
        tier_list = list(range(0, self.pattern_tier))
        keys = random.choices(tier_list, k=self.pattern_choice)
        event_list = deque()
        for key in keys:
            event_list.append(self.event_dictionary[key])
        return event_list

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


