import random

from ..utils.board import Board, create_empty_board, deep_copy
from .validators import EMPTY, SIZE, is_safe


class SudokuGame:
    def __init__(self):
        self.current = {
            'puzzle': None,
            'solution': None,
        }

    def create_empty_board(self) -> Board:
        """Return an empty Sudoku board initialized with zeros."""
        return create_empty_board()

    def deep_copy(self, board: Board) -> Board:
        """Return a deep copy of the given board."""
        return deep_copy(board)

    def is_safe(self, board: Board, row: int, col: int, num: int) -> bool:
        """Return True if placing num at (row, col) is valid."""
        return is_safe(board, row, col, num)

    def fill_board(self, board):
        for row in range(SIZE):
            for col in range(SIZE):
                if board[row][col] == EMPTY:
                    possible = list(range(1, SIZE + 1))
                    random.shuffle(possible)
                    for candidate in possible:
                        if self.is_safe(board, row, col, candidate):
                            board[row][col] = candidate
                            if self.fill_board(board):
                                return True
                            board[row][col] = EMPTY
                    return False
        return True

    def _find_empty_cell(self, board: Board) -> tuple[int, int] | None:
        for row in range(SIZE):
            for col in range(SIZE):
                if board[row][col] == EMPTY:
                    return row, col
        return None

    def _count_solutions(self, board: Board, limit: int = 2) -> int:
        empty_cell = self._find_empty_cell(board)
        if empty_cell is None:
            return 1

        row, col = empty_cell
        solutions = 0
        for candidate in range(1, SIZE + 1):
            if self.is_safe(board, row, col, candidate):
                board[row][col] = candidate
                solutions += self._count_solutions(board, limit)
                if solutions >= limit:
                    board[row][col] = EMPTY
                    return solutions
                board[row][col] = EMPTY
        return solutions

    def count_solutions(self, board: Board, limit: int = 2) -> int:
        """Return the number of solutions for a board, stopping after the limit."""
        return self._count_solutions(self.deep_copy(board), limit)

    def remove_cells(self, board: Board, clues: int) -> None:
        """Remove a number of cells from the board without preserving uniqueness."""
        attempts = SIZE * SIZE - clues
        while attempts > 0:
            row = random.randrange(SIZE)
            col = random.randrange(SIZE)
            if board[row][col] != EMPTY:
                board[row][col] = EMPTY
                attempts -= 1

    def remove_cells_with_unique_solution(self, board: Board, clues: int) -> None:
        """Remove cells while preserving a single unique solution."""
        attempts = SIZE * SIZE - clues
        cells = [(row, col) for row in range(SIZE) for col in range(SIZE)]
        random.shuffle(cells)

        while attempts > 0 and cells:
            row, col = cells.pop()
            if board[row][col] == EMPTY:
                continue

            value = board[row][col]
            board[row][col] = EMPTY
            if self.count_solutions(board) != 1:
                board[row][col] = value
            else:
                attempts -= 1

    def generate_puzzle(self, clues: int = 35) -> tuple[Board, Board]:
        """Generate a Sudoku puzzle and return it alongside its solution."""
        board = self.create_empty_board()
        self.fill_board(board)
        solution = self.deep_copy(board)
        self.remove_cells_with_unique_solution(board, clues)
        puzzle = self.deep_copy(board)
        return puzzle, solution
