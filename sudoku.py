# from game.sudoku_cell import main as run
from time import sleep
from typing import Callable

from game.fx.util.s_con import SCON
from game.util.outcome import Outcome
from game.sudoku_board import IfSB,SUDOKU_BOARD
from game.fx.sudoku_screen import SudokuScreen,SUDOKU_SCREEN

class Sudoku:
    user_quit: bool = False
    game_over: bool = False

    @staticmethod
    def main() -> int:
        Sudoku.intro()
        ss: SudokuScreen = SUDOKU_SCREEN.apply()

        while not (Sudoku.user_quit or Sudoku.game_over):
            cs: str = Sudoku.safe_input("Enter an action or an input: ")
            
            if not (cs == None) and len(cs) > 0:
                for ch in cs:
                    Sudoku.react_to_input(ch, ss)
        
        Sudoku.end_message()

        return 0
    
    @staticmethod
    def react_to_input(c: str, ss: SudokuScreen) -> None:
        nums: list[str] = ['1','2','3','4','5','6','7','8','9']
        
        if   c == SCON.right     : ss.move_caret_right()
        elif c == SCON.left      : ss.move_caret_left()
        elif c == SCON.down      : ss.move_caret_down()
        elif c == SCON.up        : ss.move_caret_up()
        elif c == 'q'            : Sudoku.user_quit = True
        elif c == 's'            : Sudoku.game_over = ss.call_sudoku_board().check_board(); None if Sudoku.game_over else Sudoku.err_message()
        elif c == '0' or c == '_': SUDOKU_SCREEN.print_at_caret_position(ss, '_') if (ss.insert_val(0) == Outcome.SUCCESS) else None
        elif c in nums           : SUDOKU_SCREEN.print_at_caret_position(ss, c) if ss.insert_val(c) == Outcome.SUCCESS else None
        else                     : None

    @staticmethod
    def safe_input(message: str) -> str:
        return SUDOKU_SCREEN.safe_input(message, SCON.bold)
    
    @staticmethod
    def err_message() -> None:
        SUDOKU_SCREEN.safe_print(                                   \
            "Your're sudoku is wrong. Please consider quitting.",   \
            f"{SCON.bRed}{SCON.white}")

    @staticmethod
    def end_message() -> None:
        if Sudoku.game_over:
            SUDOKU_SCREEN.safe_print("That is correct! Great job!", SCON.bold)
        else:
            SUDOKU_SCREEN.safe_print("That could have gone better..." +     \
                "like much better. Anyway, thanks for playing!",            \
                SCON.bold)

    @staticmethod
    def intro() -> None:
        SCON.reset_screen_and_caret()
        print("Hello World!\n\n");                      sleep(3.5)

        SCON.caret_save()
        input("[Press Enter to Exit]")
        SCON.caret_restore()
        print("Well, this is awkward...")
        print("Program execution didn't end...So...");  sleep(2.5)

        name: str = input("\nTell me, what is your name?\n")

        print(f"\nNice to meet you {SCON.bold}{name}{SCON.reset}")
        Sudoku.blocking_print((3,""))
        print("\n\nMy name is", end = "")

        Sudoku.blocking_print((7,'.'))
        print("wait for it", end = "")
        Sudoku.blocking_print((7,'.'))
        print()
        SCON.caret_save()

        Sudoku.loading_print(30, '+')
        SCON.del_line()
        SCON.caret_x_pos(0)
        SCON.caret_save()
        Sudoku.blocking_print((10,'.'))
        SCON.caret_restore()

        print("Wait for it again", end = "")
        Sudoku.blocking_print((10,"."))
        print("\n\n\n")

        Sudoku.special_print(SUDOKU_SCREEN.sudoku_banner())

        print("\n\n\n")
        print("I'm sure you'd like to play, but I've already solved it for you.");  sleep(2.5)
        print("Just trust me. I did it.");                                          sleep(2.0)
        print(f"Anyway, it's been a pleasure meeting you {SCON.bold}{name}{SCON.reset}")
        SCON.caret_save()
        input("[Press Enter to Exit]")

        SCON.caret_restore()
        print("Who am I kidding? Let's play!");                                     sleep(2.0)
        SCON.reset_screen_and_caret()

        print(SUDOKU_SCREEN.sudoku_banner() + "\n\n\n\n")
        print(SUDOKU_SCREEN.sudoku_grid())
    
    @staticmethod
    def blocking_print(rs: tuple[int,str]) -> None:
        (reps, string) = rs
        count: int = 0
        while count < reps:
            sleep(0.5)
            print(string + SCON.save)
            SCON.caret_restore()
            count += 1

    @staticmethod
    def special_print(string: str) -> None:
        start: int = 0
        end: int = 50
        step: int = 50

        while end <= len(string):
            sleep(0.1)
            print(string[start:end] + SCON.save)
            SCON.caret_restore()
            start = end
            end += step if end + step < len(string) else end + step - len(string)
    
    @staticmethod
    def loading_print(reps: int, string: str) -> None:
        f: Callable[[str],str] = lambda s: s + SCON.del_char
        end_chars: list[str] = [f('/'), f('-'),f('|'),f('\\')]
        end_chars_repeat: int = 50

        for c in range(reps):
            SCON.caret_x_pos(0)
            SCON.del_line()
            print(f"{SCON.cyan}[LOADING]{SCON.reset}", end = "")
            print(string * c, end = "")
            for repeat in range(end_chars_repeat):
                for end_char in end_chars:
                    SCON.caret_save()
                    print(end_char)
                    sleep(0.0005)
                    SCON.caret_restore()
            SCON.caret_restore()

if __name__ == "__main__":
    Sudoku.main()