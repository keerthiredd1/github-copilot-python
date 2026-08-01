"""Flask entrypoint for the Sudoku application."""

from sudoku_app import CURRENT, app


def main() -> None:
    """Run the Flask development server."""
    app.run(debug=True)


if __name__ == '__main__':
    main()
