from typing import Any, Callable, Type
from game.util.pos import Pos
from game.util.outcome import Outcome
from game.util.editable import Editable
from game.sudoku_cell import SUDOKU_CELL, SudokuCell

# from math import Random

class IfSB:
    from game.sudoku_board import IfSB

    board           : list[list[SudokuCell]]

    posIsNotEditable: Callable[[Pos],bool]
    posIsEditable   : Callable[[Pos],bool]
    isValid         : Callable[[Pos,int],bool]

    checkBoard      : Callable[[],bool]

    def apply(self: IfSB, x: int)                 -> Callable[[int],int]  : pass
    def getBoard(self: IfSB, a: Any)              -> tuple[IfSB,Any]    : pass

    def getCell(self, p: Pos)               -> SudokuCell           : pass
    def eq(self, pv: tuple[Pos,SudokuCell]) -> None                 : pass

    def insert(self, n: int, p: Pos)        -> Outcome              : pass

class _SudokuBoard:
    DEFAULT_FILL: int = 33

    board_h  : int = 9
    board_w  : int = 9
    empty_rep: str = "_"

    def apply(self, cells_to_fill: int = DEFAULT_FILL) -> IfSB:
        sb: IfSB = IfSB()
        self.editable_fill(sb)
        self.random_immutable_fill(sb, cells_to_fill)

        return sb
    
    ## random_immutable_fill needs to be re-defined because it's logic is incorrect
    def random_immutable_fill(sb: IfSB, number_of_cells_to_fill: int) -> None:
        if (number_of_cells_to_fill > 0):
            pass
        else:
            pass
    
    def editable_fill(self, sb: IfSB) -> None:
        # IfSB.board = map(lambda row: map(lambda _: SUDOKU_CELL.apply(SUDOKU_CELL.EMPTY), row),IfSB.board)
        IfSB.board = [[SUDOKU_CELL.apply(SUDOKU_CELL.EMPTY) for x in range(_SudokuBoard.boardH)] for y in range(_SudokuBoard.boardW)]


class SudokuBoard(IfSB):
    def __init__(self) -> None:
        super().__init__()
    

SUDOKU_BOARD: _SudokuBoard = _SudokuBoard()