from bullet_patterns.aimed_pattern import AimedPattern
from bullet_patterns.tri_pattern import TriPattern
from bullet_patterns.no_scope import NoScope
from bullet_patterns.homing_pattern import HomingPattern
from collections import deque
# TO-DO: Line up the event order, as in like the target will only activate movement's countdown
# after finishing a pattern. The pattern manager should be responsible for choosing the patterns from now on.
# Also, fix the tri-pattern bullet
# Yeah, the deque can be improved...


class PatternManager:
    """A class for maintaining the alien's choice of bullet patterns"""
    def __init__(self, main_game, shooter):
        self.shooter = shooter
        self.first_pattern = AimedPattern(main_game, self.shooter)
        self.second_pattern = TriPattern(main_game, self.shooter)
        self.third_pattern = NoScope(main_game, self.shooter)
        self.fourth_pattern = HomingPattern(main_game, self.shooter)
        self.event_deque = deque([self.fourth_pattern])

    def use_pattern(self):
        self.event_deque[0].shoot_burst()

    def switch_pattern(self):
        """Event queue using queue"""
        event = self.event_deque.popleft()
        event.reset()
        self.event_deque.append(event)



