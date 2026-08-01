import importlib

import pytest
from flask import Flask

import app as app_module


@pytest.fixture
def client():
    app_module.app.config.update(TESTING=True)
    with app_module.app.test_client() as client:
        yield client


def test_index_renders_homepage(client):
    response = client.get('/')

    assert response.status_code == 200
    assert '<!doctype html>' in response.get_data(as_text=True).lower()


def test_index_includes_hint_button(client):
    response = client.get('/')
    html = response.get_data(as_text=True)

    assert 'id="use-hint"' in html
    assert 'Hint' in html


def test_new_game_returns_puzzle_and_stores_solution(client):
    response = client.get('/new?clues=30')

    assert response.status_code == 200
    payload = response.get_json()

    assert 'puzzle' in payload
    assert len(payload['puzzle']) == 9
    assert app_module.CURRENT['solution'] is not None


def test_check_solution_reports_incorrect_cells_for_wrong_board(client):
    client.get('/new?clues=30')
    board = app_module.CURRENT['solution']
    wrong_board = [row[:] for row in board]
    wrong_board[0][0] = 1 if wrong_board[0][0] != 1 else 2

    response = client.post('/check', json={'board': wrong_board})

    assert response.status_code == 200
    payload = response.get_json()
    assert [0, 0] in payload['incorrect']


def test_check_solution_returns_error_when_no_game_in_progress(client):
    app_module.CURRENT['puzzle'] = None
    app_module.CURRENT['solution'] = None

    response = client.post('/check', json={'board': []})

    assert response.status_code == 400
    payload = response.get_json()
    assert payload['error'] == 'No game in progress'
