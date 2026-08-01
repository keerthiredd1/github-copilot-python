# Flask Sudoku

A polished Flask-based Sudoku game with a responsive frontend, unique-solution puzzle generation, dark mode, timer, hint support, and a browser-based leaderboard.

## Project Overview

This repository contains a Sudoku web application built with Flask and vanilla JavaScript. The game generates valid Sudoku puzzles with a unique solution, allows the player to choose difficulty, and tracks progress in a mobile-friendly interface.

## Features

- Unique-solution Sudoku puzzle generation on the server
- Difficulty selector with Easy, Medium, and Hard options
- Locked prefilled cells for puzzle clues
- Hint button reveals a correct value for one empty cell
- Check button validates the current board and highlights incorrect entries
- Timer starts when a new game is generated and stops on a correct solve
- Dark mode toggle with preference persistence
- Top 10 leaderboard saved in browser `localStorage`
- Responsive layout for desktop and mobile screens
- Flask backend with JSON endpoints for new puzzles and solution checking

## Technologies Used

- Python 3
- Flask
- HTML5
- CSS3
- JavaScript
- Browser `localStorage`

## Installation Instructions

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/github-copilot-python.git
cd github-copilot-python/starter
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

From the `starter` directory, start the Flask app:

```bash
python app.py
```

Then open the app in your browser at:

```text
http://127.0.0.1:5000
```

## Running the Test Suite

Execute the project tests with `pytest` from the `starter` directory:

```bash
python -m pytest -q
```

## Project Structure

```
starter/
├── app.py                 # Flask entry point
├── requirements.txt       # Python dependencies
├── static/                # Frontend assets
│   ├── main.js
│   └── styles.css
├── templates/             # HTML templates
│   └── index.html
├── sudoku_app/            # Application package
│   ├── __init__.py
│   ├── routes/            # Flask route definitions
│   ├── services/          # Game service layer
│   └── game/              # Sudoku game logic
└── tests/                 # Pytest test cases
```

## GitHub Copilot Usage

This project has been developed with GitHub Copilot assisting the refactor and implementation. Copilot helped with code structure, modularization, and JavaScript interaction while preserving the game behavior and test coverage.

## Copilot Evaluation

During development I reviewed GitHub Copilot's suggestions before accepting
them.

One example was a suggested refactor of the Sudoku validation logic.
Instead of accepting the generated code exactly as proposed, I reviewed the
implementation and modified it to preserve readability and maintain a clear
separation of responsibilities.

A screenshot of this interaction is included in the `Screenshots` folder.

## Screenshots

The current project does not include embedded screenshot files, but the UI is designed with a modern board layout, control panels, timer display, and leaderboard panel. Add screenshots to the repository and update this section as needed.

## Author

- GitHub Copilot-assisted project

## License

This repository is licensed under the terms included in `LICENSE.txt`.
