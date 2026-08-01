import pytest

import sudoku_logic


def test_create_empty_board_has_correct_size_and_empty_values():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert board[0][0] == sudoku_logic.EMPTY
    assert board[8][8] == sudoku_logic.EMPTY


def test_is_safe_detects_conflicts_in_row_column_and_box():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 5
    board[0][1] = 5

    assert sudoku_logic.is_safe(board, 0, 2, 5) is False
    assert sudoku_logic.is_safe(board, 2, 0, 5) is False

    board = sudoku_logic.create_empty_board()
    board[0][0] = 1
    board[1][1] = 1

    assert sudoku_logic.is_safe(board, 2, 2, 1) is False


def test_is_safe_allows_valid_placement():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 1
    board[0][1] = 2
    board[1][0] = 3

    assert sudoku_logic.is_safe(board, 2, 2, 4) is True


def test_generate_puzzle_returns_puzzle_and_solution_with_valid_dimensions():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)

    assert len(puzzle) == sudoku_logic.SIZE
    assert len(solution) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)
    assert all(len(row) == sudoku_logic.SIZE for row in solution)
    assert puzzle != solution


def test_generated_puzzle_has_a_single_unique_solution():
    puzzle, _ = sudoku_logic.generate_puzzle(clues=35)

    assert sudoku_logic.count_solutions(puzzle) == 1


def test_count_solutions_stops_after_two_solutions():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 1
    board[0][1] = 2
    board[0][2] = 3

    assert sudoku_logic.count_solutions(board, limit=2) == 2


def test_remove_cells_reduces_clue_count():
    board = sudoku_logic.create_empty_board()
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            board[i][j] = (i * 3 + j) % sudoku_logic.SIZE + 1

    sudoku_logic.remove_cells(board, clues=20)

    clues = sum(cell != sudoku_logic.EMPTY for row in board for cell in row)
    assert clues <= 20
