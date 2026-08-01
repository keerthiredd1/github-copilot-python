from ..game.logic import Board, SudokuGame


class GameService:
    def __init__(self):
        self._game = SudokuGame()
        self.current: dict[str, Board | None] = {
            'puzzle': None,
            'solution': None,
        }

    def generate_puzzle(self, clues: int = 35) -> tuple[Board, Board]:
        """Generate a new puzzle and store its state in the service."""
        puzzle, solution = self._game.generate_puzzle(clues)
        self.current['puzzle'] = puzzle
        self.current['solution'] = solution
        return puzzle, solution

    def get_solution(self) -> Board | None:
        """Return the current solution board, or None if no game exists."""
        return self.current.get('solution')
