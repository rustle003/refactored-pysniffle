from typing import TypeVar

from game.util.outcome import Outcome

T = TypeVar('T')

class AssignmentLimitation:
    def assign(self, x: T) -> Outcome:
        pass

    def is_assignable(self, x: T) -> bool:
        pass