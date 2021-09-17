from abc import abstractstaticmethod
from functools import reduce

from math import sqrt
from random import Random
from typing import Any, Callable, Generator, TypeVar

from game.util.immutable import Immutable
from game.util.pos import Pos
from game.util.outcome import Outcome
from game.util.editable import Editable
from game.sudoku_cell import SUDOKU_CELL, SudokuCell

SudokuBoard = TypeVar('SudokuBoard')

class IfSB:
    def __init__(self) -> None:
        self.board               : list[list[SudokuCell]]

        self.pos_is_not_editable : Callable[[Pos],bool]
        self.pos_is_editable     : Callable[[Pos],bool]
        self.is_valid            : Callable[[Pos,int],bool]

        self.check_board         : Callable[[],bool]

    def apply(self: 'IfSB', x: int)         -> Callable[[int],int]: pass
    def get_board(self: 'IfSB', a: Any)     ->   tuple['IfSB',Any]: pass

    def get_cell(self, p: Pos)              ->          SudokuCell: pass
    def eq(self, pv: tuple[Pos,SudokuCell]) ->                None: pass

    def insert(self, n: int, p: Pos)        ->             Outcome: pass

class _SudokuBoard(IfSB):
    DEFAULT_FILL: int = 33

    board_h  : int = 9
    board_w  : int = 9
    empty_rep: str = "_"

    def __init__(self) -> None: pass

    def apply(self, cells_to_fill: int = DEFAULT_FILL) -> IfSB:
        sb: IfSB = SudokuBoard()
        self.editable_fill(sb)
        self.random_immutable_fill(sb, cells_to_fill)

        return sb
    
    ## random_immutable_fill needs to be re-defined because it's logic is incorrect
    def random_immutable_fill(self, sb: IfSB, number_of_cells_to_fill: int) -> None:
        if (number_of_cells_to_fill > 0):
            ecs: list[Pos] = self.get_editable_cells(sb)
            check_valid: Callable[[Pos,int],bool] = self.BoardChecker.assert_lacks(sb)
            pos_select: int = self.generate_number(0,len(ecs) - 1)

            while(self.cell_is_not_immutable(sb, ecs[pos_select])):
                value: int = self.generate_val()

                if check_valid(ecs[pos_select],value):
                    sb.board[ecs[pos_select].x][ecs[pos_select].y] = SUDOKU_CELL.apply(value,True)

            self.random_immutable_fill(sb, number_of_cells_to_fill - 1)
    
    def editable_fill(self, sb: IfSB) -> None:
        sb.board = [[SUDOKU_CELL.apply(SUDOKU_CELL.EMPTY) for y in range(_SudokuBoard.board_w)] for x in range(_SudokuBoard.board_h)]

    def get_editable_cells(self, sb: IfSB) -> list[Pos]:
        return reduce(lambda l1,l2: l1 + l2, [[Pos(row, col) \
            for col in range(_SudokuBoard.board_w) if self.cell_is_not_immutable(sb,Pos(row,col))] \
            for row in range(_SudokuBoard.board_h)])
    
    def cell_is_not_immutable(self, sb: IfSB, pos: Pos) -> bool:
        return not self.BoardChecker.board_position_is_immutable(sb)(pos)
    
    def generate_number(self, start: int, end: int) -> int:
        return (int(Random().random() * 10 * (end + 1)) + start * 10) // 10
    
    def generate_sb_number(self, n: int) -> int:
        return self.generate_number(n, _SudokuBoard.board_h -1)
    
    def generate_pos(self) -> Pos:
        return Pos(self.generate_sb_number(0), self.generate_sb_number(0))
    
    def generate_val(self) -> int:
        return self.generate_sb_number(1)
    
    class BoardChecker:
        def board_position_is_immutable(sb: IfSB) -> Callable[[Pos],bool]:
            return lambda pos: isinstance(sb.get_cell(pos),Immutable)
        
        def board_position_is_editable(sb: IfSB) -> Callable[[Pos],bool]:
            return lambda pos: isinstance(sb.get_cell(pos),Editable)
        
        def assert_lacks(sb: IfSB) -> Callable[[Pos,int],bool]:
            ROW   : _SudokuBoard.Row    = _SudokuBoard.Row
            COLUMN: _SudokuBoard.Column = _SudokuBoard.Column
            SQUARE: _SudokuBoard.Square = _SudokuBoard.Square

            CHECK: Callable[[IfSB,int,list[Pos]],bool] = _SudokuBoard.BoardChecker.check

            return  lambda pos,val:                             \
                    CHECK(sb,val,ROW.that_includes(pos))    and \
                    CHECK(sb,val,COLUMN.that_includes(pos)) and \
                    CHECK(sb,val,SQUARE.that_includes(pos))

        def check(sb: IfSB, val: int, poss: list[Pos]) -> bool:
            return val not in map(lambda pos: sb.apply(pos.x)(pos.y), poss)
        
        def check_all(sb: IfSB) -> bool:
            return _SudokuBoard.BoardChecker.is_filled_completely(sb, _SudokuBoard.FullBoard.apply()) and   \
                False not in (_SudokuBoard.BoardChecker.is_unique_sequence(sb,pos)                          \
                for pos in _SudokuBoard.FullBoard.all_positions)
        
        def is_filled_completely(sb: IfSB, sq: list[Pos]) -> bool:
            return SUDOKU_CELL.EMPTY not in (sb.get_cell(pos).value() for pos in sq)
        
        def is_unique_sequence(sb: IfSB, sq: list[Pos]) -> bool:
            if len(sq) < 2:
                return True
            else:
                h_pos   : Pos = sq[0]
                t_poss  : list[Pos] = sq[1::]
                return sb.apply(h_pos.x)(h_pos.y) not in (sb.apply(pos.x)(pos.y) for pos in t_poss)\
                    and _SudokuBoard.BoardChecker.is_unique_sequence(sb, t_poss)

    class SudokuBoardVirtualPartition:
        @abstractstaticmethod
        def apply(n: int) -> list[Pos]: pass
        
        @abstractstaticmethod
        def that_includes(pos: Pos) -> list[Pos]: pass
    
    class Row(SudokuBoardVirtualPartition):
        def apply(n: int) -> list[Pos]:
            return _SudokuBoard.Row.that_includes(Pos(n,0))
        
        def that_includes(pos: Pos) -> list[Pos]:
            return [Pos(pos.x, y) for y in range(_SudokuBoard.board_h)]

    class Column(SudokuBoardVirtualPartition):
        def apply(n: int) -> list[Pos]:
            _SudokuBoard.Column.that_includes(Pos(0,n))
        
        def that_includes(pos: Pos) -> list[Pos]:
            return [Pos(x, pos.y) for x in range(_SudokuBoard.board_w)]
        
    class Square(SudokuBoardVirtualPartition):
        def square_dim() -> int: return int(sqrt(_SudokuBoard.board_h))

        def apply(n: int) -> list[Pos]: 
            return _SudokuBoard.Square._apply(\
                _SudokuBoard.Square.flat_transform(n))
        
        def _apply(pos: Pos) -> list[Pos]:
            return _SudokuBoard.Square._apply_(pos.x,pos.y)
        
        def _apply_(x: int, y: int) -> list[Pos]:
            return _SudokuBoard.Square.that_includes(Pos(   \
                _SudokuBoard.Square.revert(x),              \
                _SudokuBoard.Square.revert(y)))

        def that_includes(pos: Pos) -> list[Pos]:
            row_transform: Callable[[int],int] = _SudokuBoard.Square.transform(pos.x)
            col_transform: Callable[[int],int] = _SudokuBoard.Square.transform(pos.y)

            return reduce(lambda l1,l2: l1 + l2,                            \
                    [[Pos(row_transform(r),col_transform(c))                \
                    for c in range(_SudokuBoard.Square.square_dim())]       \
                    for r in range(_SudokuBoard.Square.square_dim())])

        def transform(n: int) -> Callable[[int],int]:
            return lambda m: m // _SudokuBoard.Square.square_dim() *  \
                                _SudokuBoard.Square.square_dim() + n
        
        def revert(n: int) -> int:
            return n * _SudokuBoard.Square.square_dim()
        
        def flat_transform(n: int) -> Pos:
            return Pos(n // _SudokuBoard.Square.square_dim(),\
                        n % _SudokuBoard.Square.square_dim())

    class FullBoard:
        def square_dim() -> int: return _SudokuBoard.board_h

        def apply() -> list[Pos]: return _SudokuBoard.FullBoard.contains_all()

        def all_positions() -> list[list[Pos]]:
            ROW   : _SudokuBoard.SudokuBoardVirtualPartition = _SudokuBoard.Row
            COLUMN: _SudokuBoard.SudokuBoardVirtualPartition = _SudokuBoard.Column
            SQUARE: _SudokuBoard.SudokuBoardVirtualPartition = _SudokuBoard.Square

            return [reduce(lambda l1,l2: l1 if l2 == None else l1 + l2, [part.apply(idx) for part in [ROW,COLUMN,SQUARE]])      \
                    for idx in range(_SudokuBoard.FullBoard.square_dim())]
        
        def contains_all() -> list[Pos]:
            return reduce(lambda l1,l2: l1 + l2, \
                    _SudokuBoard.FullBoard.all_positions())

    def main(self) -> int:
        print("Testing sudoku_board.py")

        sb: IfSB = _SudokuBoard.apply(self)
        check_test: Callable[[Pos,int],bool] = _SudokuBoard.BoardChecker.assert_lacks(sb)
        check_val: int = 23
        expected_result: bool = False

        sb.eq((Pos(8,0),SUDOKU_CELL.apply(23,True)))

        for r in range(_SudokuBoard.board_h):
            for c in range(_SudokuBoard.board_w):
                print(sb.apply(r)(c),end = '')
            print()
        
        print(f'Does the lower left corner not contain {check_val}: {check_test(Pos(8,0),check_val)}')
        if expected_result == check_test(Pos(8,0),check_val):
            print("Coner test: PASS")
        else:
            print("Corner test: FAIL")
        
        expected_result: bool = False
        result: bool = _SudokuBoard.BoardChecker.is_unique_sequence(sb, _SudokuBoard.Square.that_includes(Pos(0,5)))

        print(f"Checking is_unique_seq function -> Expected result: {expected_result} -> (actual value): {result}")
        if expected_result == result:
            print("Uniqueness test: PASS")
        else:
            print("Uniqueness test: FAIL")


SUDOKU_BOARD: _SudokuBoard = _SudokuBoard()


class SudokuBoard(IfSB):
    def __init__(self) -> None:
        super().__init__()
        self.pos_is_not_editable : Callable[[Pos],bool]     = SUDOKU_BOARD.BoardChecker.board_position_is_immutable(self)
        self.pos_is_editable     : Callable[[Pos],bool]     = SUDOKU_BOARD.BoardChecker.board_position_is_editable(self)
        self.is_valid            : Callable[[Pos,int],bool] = SUDOKU_BOARD.BoardChecker.assert_lacks(self)

        self.check_board         : Callable[[],bool]        = lambda : SUDOKU_BOARD.BoardChecker.check_all(self)

    def apply(self: IfSB, x: int) -> Callable[[int], int]:
        return lambda y: self.board[x][y].value()
    
    def get_cell(self, p: Pos) -> SudokuCell:
        return self.board[p.x][p.y]
    
    def eq(self, pv: tuple[Pos, SudokuCell]) -> None:
        self.board[pv[0].x][pv[0].y] = pv[1]
    
    def insert(self, n: int, p: Pos) -> Outcome:
        if self.pos_is_not_editable(p):
            return Outcome.FAILURE
        elif self.pos_is_editable(p):
            return self.get_cell(p).assign(n)
        else:
            self.eq((p,SUDOKU_CELL(n)))
            return Outcome.SUCCESS
    
if __name__ == "__main__":
    SUDOKU_BOARD.main()
