Board = list[list[int]]
SIZE = 9
EMPTY = 0


def is_safe(board: Board, row: int, col: int, num: int) -> bool:
    """Return True if num can be placed at (row, col) without conflicts."""
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True
