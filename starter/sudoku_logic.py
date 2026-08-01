from sudoku_app.game.logic import Board, EMPTY, SIZE, SudokuGame

_game = SudokuGame()


def deep_copy(board: Board) -> Board:
    """Return a deep copy of the given board."""
    return _game.deep_copy(board)


def create_empty_board() -> Board:
    """Return an empty 9x9 Sudoku board."""
    return _game.create_empty_board()


def is_safe(board: Board, row: int, col: int, num: int) -> bool:
    """Return True if num is safe to place at the given cell."""
    return _game.is_safe(board, row, col, num)


def fill_board(board: Board) -> bool:
    """Fill the board with a completed Sudoku solution."""
    return _game.fill_board(board)


def remove_cells(board: Board, clues: int) -> None:
    """Remove cells from the board leaving the desired number of clues."""
    return _game.remove_cells(board, clues)


def count_solutions(board: Board, limit: int = 2) -> int:
    """Count the number of solutions for a board, stopping at the limit."""
    return _game.count_solutions(board, limit=limit)


def generate_puzzle(clues: int = 35) -> tuple[Board, Board]:
    """Generate a new puzzle and its full solution."""
    return _game.generate_puzzle(clues)
