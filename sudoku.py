from game.sudoku_cell import main as run
from game.sudoku_board import SUDOKU_BOARD

user_quit: bool = False
game_over: bool = False

def main() -> int:
    run()
    return SUDOKU_BOARD.main()

if __name__ == "__main__":
    main()