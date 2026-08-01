import copy

Board = list[list[int]]
SIZE = 9
EMPTY = 0


def deep_copy(board: Board) -> Board:
    """Return a deep copy of the provided Sudoku board."""
    return copy.deepcopy(board)


def create_empty_board() -> Board:
    """Create an empty 9x9 Sudoku board filled with EMPTY cells."""
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def count_clues(board: Board) -> int:
    """Return the count of non-empty cells on the board."""
    return sum(cell != EMPTY for row in board for cell in row)
