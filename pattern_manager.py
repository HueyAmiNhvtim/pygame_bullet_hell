import pygame
import numpy
from straight_pattern import StraightPattern
from tri_pattern import TriPattern
from collections import deque


class PatternManager:
    """A class for maintaining the alien's choice of bullet patterns"""

    def __init__(self, main_game, shooter):
        self.shooter = shooter
        self.first_pattern = StraightPattern(main_game, self)
        self.second_pattern = TriPattern(main_game, self)
        self.event_deque = deque([self.first_pattern])

    def use_pattern(self):
        """Make sure to check for remaining burst in the last pattern! Maybe implement burst cooldown later"""
        if self.shooter.movement_disabled or self.event_deque[0].burst_left == 0:
            event = self.event_deque.pop()
            event.reset()
            self.event_deque.appendleft(event)
        self.event_deque[0].shoot_burst()


