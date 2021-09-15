from abc import abstractstaticmethod
from functools import reduce

from math import sqrt
from random import Random
from typing import Any, Callable, Generator, Type
from typing_extensions import TypeAlias

from game.util.immutable import Immutable
from game.util.pos import Pos
from game.util.outcome import Outcome
from game.util.editable import Editable
from game.sudoku_cell import SUDOKU_CELL, SudokuCell



SB: TypeAlias = '_SudokuBoard'

class IfSB:
    from game.sudoku_board import IfSB

    board               : list[list[SudokuCell]]

    pos_is_not_editable : Callable[[Pos],bool]
    pos_is_editable     : Callable[[Pos],bool]
    is_valid            : Callable[[Pos,int],bool]

    check_board         : Callable[[],bool]

    def apply(self: IfSB, x: int)           -> Callable[[int],int]: pass
    def get_board(self: IfSB, a: Any)       ->     tuple[IfSB,Any]: pass

    def get_cell(self, p: Pos)              ->          SudokuCell: pass
    def eq(self, pv: tuple[Pos,SudokuCell]) ->                None: pass

    def insert(self, n: int, p: Pos)        ->             Outcome: pass

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
    def random_immutable_fill(self, sb: IfSB, number_of_cells_to_fill: int) -> None:
        if (number_of_cells_to_fill > 0):
            pass
        else:
            pass
    
    def editable_fill(self, sb: IfSB) -> None:
        IfSB.board = [[SUDOKU_CELL.apply(SUDOKU_CELL.EMPTY) for y in range(_SudokuBoard.board_w)] for x in range(_SudokuBoard.board_h)]

    def get_editable_cells(self, sb: IfSB) -> Generator[Pos]:
        for r,c in ((row,col) for col in range(_SudokuBoard.board_w) for row in range(_SudokuBoard.board_h)):
            yield sb.apply(r)(c)
    
    def cell_is_not_immutable(self, bp: tuple[IfSB,Pos]) -> bool:
        (sb, pos) = bp
        return not self.BoardChecker.board_position_is_immutable(sb)(pos)
    
    def generate_number(self, start: int, end: int) -> int:
        return (int(Random() * 10 * (end + 1) - 1) + start * 10) // 10
    
    def generate_sb_number(self, n: int) -> int:
        return self.generate_number(n, _SudokuBoard.board_h -1)
    
    def generate_pos(self) -> Pos:
        return Pos(self.generate_sb_number(0), self.generate_sb_number(0))
    
    def generate_val(self) -> int:
        return self.generate_sb_number(1)
    
    class BoardCheker:
        def board_position_is_immutable(sb: IfSB, pos: Pos) -> bool:
            return isinstance(sb.get_cell(pos),Immutable)
        
        def board_position_is_editable(sb: IfSB, pos: Pos) -> bool:
            return isinstance(sb.get_cell(pos),Editable)
        
        ## Needs to be defined
        def assertLacks(sb: IfSB, pos: Pos, val: int) -> bool:
            pass

        def check(sb: IfSB, val: int, poss: list[Pos]) -> bool:
            return val not in map(lambda pos: sb(pos.x, pos.y), poss)
        
        def check_all(sb: IfSB) -> bool:
            return _SudokuBoard.BoardCheker.is_filled_completely(sb) and            \
                False not in (_SudokuBoard.BoardCheker.is_unique_sequence(sb,pos)   \
                for pos in _SudokuBoard.FullBoard.all_positions)
        
        def is_filled_completely(sb: IfSB, sq: list[Pos]) -> bool:
            SUDOKU_CELL.EMPTY not in (sb.get_cell(pos).value() for pos in sq)
        
        def is_unique_sequence(sb: IfSB, sq: list[Pos]) -> bool:
            if len(sq) < 2:
                return True
            else:
                h_pos   : Pos = sq[0]
                t_poss  : list[Pos] = sq[1::]
                return sb(h_pos.x,h_pos.y) not in (sb(pos.x,pos.y) for pos in t_poss)\
                    and _SudokuBoard.BoardCheker.is_unique_sequence(sb, t_poss)

    class SudokuBoardVirtualParition:
        @abstractstaticmethod
        def apply(n: int) -> list[Pos]: pass
        
        @abstractstaticmethod
        def that_contains(pos: Pos) -> list[Pos]: pass
    
    class Row(SB.SudokuBoardVirtualPartition):
        def apply(n: int) -> list[Pos]:
            return SB.Row.that_contains(Pos(n,0))
        
        def that_contains(pos: Pos) -> list[Pos]:
            return [Pos(pos.x, y) for y in range(_SudokuBoard.board_h)]

    class Column(SB.SudokuBoardVirtualParition):
        def apply(n: int) -> list[Pos]:
            SB.Column.that_contains(Pos(0,n))
        
        def that_contains(pos: Pos) -> list[Pos]:
            return [Pos(x, pos.y) for x in range(_SudokuBoard.board_w)]
        
    class Square(SB.SudokuBoardVirtualParition):
        square_dim: int = int(sqrt(SB.board_h))

        def apply(n: int) -> list[Pos]: 
            return _SudokuBoard.Square._apply(\
                _SudokuBoard.Square.flat_transform(n))
        
        def _apply(pos: Pos) -> list[Pos]:
            return _SudokuBoard.Square._apply_(pos.x,pos.y)
        
        def _apply_(x: int, y: int) -> list[Pos]:
            return _SudokuBoard.Square.that_contains(Pos(   \
                _SudokuBoard.Square.revert(x),              \
                _SudokuBoard.Square.revert(y)))

        def that_contains(pos: Pos) -> list[Pos]:
            (x,y) = pos
            row_transform: Callable[[int],int] = _SudokuBoard.Square.transform(x)
            col_transform: Callable[[int],int] = _SudokuBoard.Square.transform(y)

            return reduce(lambda l1,l2: l1.extend(l2),              \
                    [[Pos(row_transform(r),col_transform(c))        \
                    for c in range(_SudokuBoard.Square.square_dim)] \
                    for r in range(_SudokuBoard.Square.square_dim)])

        def transform(n: int) -> Callable[[int],int]:
            return lambda m: m // _SudokuBoard.Square.square_dim *  \
                                _SudokuBoard.Square.square_dim + n
        
        def revert(n: int) -> int:
            return n * _SudokuBoard.Square.square_dim
        
        def flat_transform(n: int) -> Pos:
            return Pos(n // _SudokuBoard.Square.square_dim,\
                        n % _SudokuBoard.Square.square_dim)

    class FullBoard:
        square_dim: int = SB.board_h

        def apply() -> list[Pos]: return _SudokuBoard.FullBoard.contains_all()

        def all_positions() -> list[list[Pos]]:
            ROW   : _SudokuBoard.SudokuBoardVirtualParition = _SudokuBoard.Row
            COLUMN: _SudokuBoard.SudokuBoardVirtualParition = _SudokuBoard.Column
            SQUARE: _SudokuBoard.SudokuBoardVirtualParition = _SudokuBoard.Square

            return [[part.apply(idx) for part in [ROW,COLUMN,SQUARE]]\
                    for idx in range(_SudokuBoard.FullBoard.square_dim)]

SUDOKU_BOARD: _SudokuBoard = _SudokuBoard()

class SudokuBoard(IfSB):
    def __init__(self) -> None:
        super().__init__()
    
