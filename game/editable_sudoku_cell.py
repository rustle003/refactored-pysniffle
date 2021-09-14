from game.sudoku_cell import SudokuCell
from game.util.outcome import Outcome
from game.util.editable import Editable
from game.util.assignment_limitation import AssignmentLimitation

class EditableSudokuCell(SudokuCell,Editable,AssignmentLimitation):
    def __init__(self, val: int) -> None:
        SudokuCell.__init__(self,val)
        Editable.__init__(self)
    
    def value(self) -> int:
        return self.val

    def assign(self, x: int) -> Outcome:
        if(self.is_assignable(x)):
            self.val = x
            return Outcome.SUCCESS
        else:
            return Outcome.FAILURE

    def is_assignable(self, x: int) -> bool:
        return 0 <= x and x < 10