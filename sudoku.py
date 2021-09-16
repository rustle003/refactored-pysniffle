from game.sudoku_cell import main as run
from game.sudoku_board import SUDOKU_BOARD
from game.fx.sudoku_screen import SUDOKU_SCREEN

user_quit: bool = False
game_over: bool = False

def main() -> int:
    # run()
    # SUDOKU_BOARD.main()
    return SUDOKU_SCREEN.main()

if __name__ == "__main__":
    main()