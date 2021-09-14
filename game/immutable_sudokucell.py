from game.sudoku_cell import SudokuCell
from game.util.immutable import Immutable
from game.util.outcome import Outcome
from game.util.assignment_limitation import AssignmentLimitation

class ImmutableSudokuCell(SudokuCell,Immutable,AssignmentLimitation):
    def __init__(self, val: int) -> None:
        SudokuCell.__init__(self,val)
        Immutable.__init__(self)
    
    def value(self) -> int:
        return self.val
    
    def assign(self, x: int) -> Outcome:
        return Outcome.FAILURE
    
    def is_assignable(self, x: int) -> bool:
        return Outcome.FAILURE.getState()