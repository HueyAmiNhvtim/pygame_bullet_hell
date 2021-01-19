from straight_pattern import StraightPattern
from tri_pattern import TriPattern
from collections import deque
# TO-DO: Line up the event order, as in like the target will only activate movement's countdown
# after finishing a pattern. The pattern manager should be responsible for choosing the patterns from now on.


class PatternManager:
    """A class for maintaining the alien's choice of bullet patterns"""

    def __init__(self, main_game, shooter):
        self.shooter = shooter
        self.first_pattern = StraightPattern(main_game, self)
        self.second_pattern = TriPattern(main_game, self)
        self.event_deque = deque([self.first_pattern])
        self.burst_finished = False

    def use_pattern(self):
        """Make sure to check for remaining burst in the last pattern! Maybe implement burst cooldown later.
        Now I have to care about order of events happening, specifically about movement cooldown..."""
        if self.shooter.movement_disabled or self.event_deque[0].burst_left == 0:
            event = self.event_deque.pop()
            event.reset()
            self.event_deque.appendleft(event)
        self.event_deque[0].shoot_burst()


