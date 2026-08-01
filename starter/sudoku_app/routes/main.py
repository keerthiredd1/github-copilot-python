from flask import Blueprint, current_app, jsonify, render_template, request

bp = Blueprint('main', __name__)


def _parse_clues(value: str | None) -> int | None:
    try:
        return int(value) if value is not None else 35
    except (TypeError, ValueError):
        return None


def _validate_board(board) -> bool:
    if not isinstance(board, list) or len(board) != 9:
        return False
    return all(isinstance(row, list) and len(row) == 9 for row in board)


@bp.route('/')
def index():
    """Render the Sudoku homepage."""
    return render_template('index.html')


@bp.route('/new')
def new_game():
    """Generate a new puzzle and return it as JSON."""

    difficulty = request.args.get("difficulty", "medium")

    clue_map = {
        "easy": 42,
        "medium": 34,
        "hard": 28
    }

    clues = clue_map.get(difficulty, 34)

    game_service = current_app.extensions["game_service"]
    game_service.generate_puzzle(clues)

    return jsonify({
        "puzzle": game_service.current["puzzle"],
        "solution": game_service.current["solution"]
    })


@bp.route('/check', methods=['POST'])
def check_solution():
    """Validate the posted board against the current solution."""
    game_service = current_app.extensions['game_service']
    solution = game_service.get_solution()
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    data = request.get_json(silent=True)
    if not data or 'board' not in data:
        return jsonify({'error': 'Invalid board data'}), 400

    board = data['board']
    if not _validate_board(board):
        return jsonify({'error': 'Invalid board data'}), 400

    incorrect = []
    for i in range(9):
        for j in range(9):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({'incorrect': incorrect})
@bp.route('/hint', methods=['POST'])
def get_hint():
    """Return one correct value for an empty cell."""

    game_service = current_app.extensions["game_service"]

    puzzle = game_service.current.get("puzzle")
    solution = game_service.current.get("solution")

    if puzzle is None or solution is None:
        return jsonify({"error": "No game in progress"}), 400

    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0:
                value = solution[row][col]
                puzzle[row][col] = value

                return jsonify({
                    "row": row,
                    "col": col,
                    "value": value
                })

    return jsonify({"error": "No hints available"}), 400

def register_routes(app):
    app.register_blueprint(bp)
