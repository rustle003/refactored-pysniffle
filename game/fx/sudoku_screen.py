from typing import Any, Callable, TypeVar
from time import sleep

from game.sudoku_board import IfSB,SUDOKU_BOARD
from game.sudoku_cell import SudokuCell,SUDOKU_CELL
from game.util.pos import Pos
from game.util.outcome import Outcome
from game.fx.util.s_con import SCON

class SudokuScreen:
    pass

class _SudokuScreen_(SudokuScreen):
    def __init__(self: '_SudokuScreen_') -> None:
        console_color: Callable[[int], str] = lambda n: f"{SCON.eb}{n}m"

        self.g = console_color(32);         self.G = console_color(42)
        self.r = console_color(31);         self.R = console_color(41)
        self.m = console_color(35);         self.M = console_color(45)
        self.b = console_color(34);         self.B = console_color(44)
        self.w = console_color(37);         self.W = console_color(47)
        self.c = console_color(36);         self.C = console_color(46)
        self.k = console_color(30);         self.K = console_color(40)
        self.o = console_color( 0);         self.O = console_color( 1)

        self.xy = Pos(35,10)
        self.dx = 4
        self.dy = 2
        self.init_x_offset = 2
        self.init_y_offset = 1

        self.safe_print_pos = Pos(15, 40)
    
    def apply(self: '_SudokuScreen_') -> SudokuScreen:
        sb = SudokuScreen(SUDOKU_BOARD.apply())
        sb.initial_fill()
        _SudokuScreen_.reset_caret_position
        _SudokuScreen_.reset_console_formatting
        return sb
    
    def sudoku_grid(self: '_SudokuScreen_') -> str:
        j: int = self.xy.y - 1
        i: int = self.xy.x

        def pxy() -> str:
            nonlocal j
            j += 1
            return f"{SCON.eb}{j};{i}H"
        
        f: str = self.g
        B: str = self.G
        o: str = self.o

        return \
        f"""
        {pxy()}{f}{B}|-----------o-----------o-----------|{o}
        {pxy()}{f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}
        {pxy()}{f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}    -> Use your {self.c}arrow keys{o} to move
        {pxy()}{f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}
        {pxy()}{f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}    -> Press {self.g}s{o} to submit your sudoku
        {pxy()}{f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}
        {pxy()}{f}{B}|-----------o-----------o-----------|{o}
        {pxy()}{f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}    -> Press {self.r}q{o} to quit
        {pxy()}{f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}
        {pxy()}{f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}
        {pxy()}{f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}
        {pxy()}{f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}
        {pxy()}{f}{B}|-----------o-----------o-----------|{o}
        {pxy()}{f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}
        {pxy()}{f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}
        {pxy()}{f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}
        {pxy()}{f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}
        {pxy()}{f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}           {f}{B}|{o}
        {pxy()}{f}{B}|-----------o-----------o-----------|{o}
        """     

    def sudoku_banner(self) -> str:
        O: str = self.O
        G: str = self.G
        m: str = self.m
        C: str = self.C
        c: str = self.c
        b: str = self.b
        R: str = self.R
        W: str = self.W
        r: str = self.r
        M: str = self.M
        w: str = self.w
        o: str = self.o

        return \
        f"""
        {G}{m}  ____            _       _                                                                {o}
        {C}{b} / ___| _   _  __| | ___ | | ___   _                                                       {o}
        {R}{c} \\___ \\| | | |/ _` |/ _ \\| |/ / | | |                                                      {o}
        {W}{r}  ___) | |_| | (_| | (_) |   <| |_| |                                                      {o}
        {M}{w} |____/ \\__,_|\\__,_|\\___/|_|\\_\\\\__,_|                                                      {o}
        {o}
        """

    def coordinate_transform(self: '_SudokuScreen_',p: Pos) -> Pos:
        return Pos(p.x * self.dx + self.init_x_offset + self.xy.x,  \
                    p.y * self.dy + self.init_y_offset + self.xy.y)
    
    def print_to_screen(self: '_SudokuScreen_',pv: tuple[Pos,Any], fmt: str = "") -> None:
        (pos,a) = pv
        (r,z) = pos.unapply()

        SCON.caret_to(r,z)
        print(f"{fmt}{a}", end = "")
    
    def print_at_caret_position(self: '_SudokuScreen_',ss: SudokuScreen, a: Any, fmt: str = "") -> None:
        (tx, ty) = self.coordinate_transform(ss.caret).unapply()
        SCON.caret_to(tx,ty)
        print(f"{fmt}{a}", end = "")
    
    def safe_print(self: '_SudokuScreen_',message: str, fmt: str = "") -> None:
        (i,j) = self.safe_print_pos.unapply()
        SCON.caret_to(i, j)
        print(f"{fmt}{message}");               sleep(2.5)
        self.reset_console_formatting()
        SCON.caret_to(i,j)
        SCON.del_line()

    def safe_input(self: '_SudokuScreen_', message: str, fmt: str = "") -> str:
        (i,j) = self.safe_print_pos.unapply()
        SCON.caret_to(i,j)

        res: str = input(f"{fmt}{message}{self.o}")

        SCON.caret_to(i,j)
        SCON.del_line
        return res

    def reset_caret_position(self: '_SudokuScreen_') -> None:
        (i,j) = self.coordinate_transform(Pos(0,0))
        SCON.caret_to(i,j)
    
    def reset_console_formatting(self: '_SudokuScreen_') -> None:
        print(self.o, end = "")
    
    def guard_bounds(self: '_SudokuScreen_', nb: tuple[int,bool]) -> bool:
        (n,b) = nb
        return (0 < n and n < self.predecessor(SUDOKU_BOARD.board_h)) or b
    
    def guarded_successor(self: '_SudokuScreen_', n: int) -> int:
        return self.successor(n) \
                if self.guard_bounds((n, n == 0)) else n
    
    def guarded_predecessor(self: '_SudokuScreen_', n: int) -> int:
        return self.predecessor(n) if self.guard_bounds((n,n == self.predecessor(SUDOKU_BOARD.board_h))) else n
    
    def successor(self: '_SudokuScreen_', n: int) -> int:
        return n + 1
    
    def predecessor(self: '_SudokuScreen_', n: int) -> int:
        return n - 1
    
    def main(self: '_SudokuScreen_') -> int:
        print(f"{self.g}{self.r}Hello from _SudokuScreen_\u00B2")
        print(self.sudoku_banner())
        print(self.sudoku_grid())

SUDOKU_SCREEN: _SudokuScreen_ = _SudokuScreen_()

class SudokuScreen:
    def __init__(self: 'SudokuScreen', sBoard: IfSB) -> None:
        self.sBoard: IfSB = sBoard
        self.caret: Pos = Pos(0,0)
    
    def initial_fill(self: 'SudokuScreen') -> None:
        for r in range(SUDOKU_BOARD.board_h):
            for c in range(SUDOKU_BOARD.board_w):
                if self.sBoard.apply(r)(c) != SUDOKU_CELL.EMPTY:
                    SUDOKU_SCREEN.print_to_screen((                     \
                        SUDOKU_SCREEN.coordinate_transform(Pos(r,c)),   \
                        self.sBoard.apply(r)(c)),                       \
                        SUDOKU_SCREEN.r)

        for r in range(SUDOKU_BOARD.board_h):
            for c in range(SUDOKU_BOARD.board_w):
                if self.sBoard.apply(r)(c) == SUDOKU_CELL.EMPTY:
                    SUDOKU_SCREEN.print_to_screen((                     \
                        SUDOKU_SCREEN.coordinate_transform(             \
                        Pos(r,c)),                                      \
                        SUDOKU_BOARD.empty_rep),                        \
                        SUDOKU_SCREEN.w)

    def insert_val(self: 'SudokuScreen', a: Any) -> Outcome:
        return self.sBoard.insert(int(a.__str__()), self.caret)
    
    def call_sudoku_board(self: 'SudokuScreen') -> IfSB:
        return self.sBoard
    
    def caret_to_pos(self: 'SudokuScreen') -> Pos:
        return Pos(self.caret.x, self.caret.y)
    
    def move_caret_right(self: 'SudokuScreen') -> None:
        self.caret.x = SUDOKU_SCREEN.guarded_successor(self.caret.x)
        self.move_caret()

    def move_caret_left(self: 'SudokuScreen') -> None:
        self.caret.x = SUDOKU_SCREEN.guarded_predecessor(self.caret.x)
        self.move_caret()
    
    def move_caret_down(self: 'SudokuScreen') -> None:
        self.caret.y = SUDOKU_SCREEN.guarded_successor(self.caret.y)
        self.move_caret()
    
    def move_caret_up(self: 'SudokuScreen') -> None:
        self.caret.y = SUDOKU_SCREEN.guarded_predecessor(self.caret.y)
        self.move_caret()
    
    def move_caret(self: 'SudokuScreen') -> None:
        (r,z) = SUDOKU_SCREEN.coordinate_transform(self.caret).unapply()
        SCON.caret_to(r,z); sleep(0.025)