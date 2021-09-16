from game.util.editable import Editable
from game.util.immutable import Immutable
from typing import Generic

from game.util.assignment_limitation import AssignmentLimitation,T

class SudokuCell(Generic[T],AssignmentLimitation):
    def __init__(self,val: T) -> None:
        Generic[T].__init__(self,None)
        AssignmentLimitation.__init__(self)
        self.val = val
    
    def value(self) -> T: pass

class _SudokuCell(SudokuCell):
    from game.editable_sudoku_cell import EditableSudokuCell
    from game.immutable_sudokucell import ImmutableSudokuCell

    EMPTY: int = 0
    
    def __init__(self: '_SudokuCell', val: T = None) -> None:
        SudokuCell.__init__(self,val)

    def apply(self: '_SudokuCell', value: T, b: bool = False) -> SudokuCell:
        if(not b):
            return self.EditableSudokuCell(value)
        else:
            return self.ImmutableSudokuCell(value)

SUDOKU_CELL: _SudokuCell = _SudokuCell()

def main() -> int:
    print("Hello from SudokuCell")

    test: _SudokuCell = SUDOKU_CELL.apply(5, True)

    print(test.value())

    test.assign(3)

    print(test.value())

    print(isinstance(test, Editable))

    return 0