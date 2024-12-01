import random
import pytest

from games.api import Move, app
from fastapi.testclient import TestClient

random.seed(42)


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_move():
    move = Move(x=1, y=2)
    assert move.x == 1
    assert move.y == 2

    with pytest.raises(ValueError):
        move = Move(x="a", y="b")

    with pytest.raises(ValueError):
        move = Move(x=-1, y=0)

    with pytest.raises(ValueError):
        move = Move(x=0, y=3)


def test_create_game(client):
    response = client.post("/games/")
    assert response.status_code == 200
    game_id = response.json()
    assert game_id


def test_make_move(client):
    response = client.post("/games/")
    game_id = response.json()
    response = client.post(f"/games/{game_id}/move/", json={"x": 0, "y": 0})
    assert response.status_code == 200
    assert response.json() == {
        "result": (
            "Player X made a move at (0, 0)\n"
            "Player O made a move at (0, 2)\n"
            "X|.|O\n"
            ".|.|.\n"
            ".|.|."
        )
    }

    response = client.post(f"/games/{game_id}/move/", json={"x": 0, "y": 0})
    assert response.status_code == 200
    assert "Invalid move: (0, 0)" in response.text

    response = client.post(f"/games/{game_id}/move/", json={"x": 0, "y": 1})
    assert response.status_code == 200
    assert response.json() == {
        "result": (
            "Player X made a move at (0, 1)\n"
            "Player O made a move at (1, 0)\n"
            "X|X|O\n"
            "O|.|.\n"
            ".|.|."
        )
    }

    response = client.post(f"/games/{game_id}/move/", json={"x": 1, "y": 1})
    assert response.status_code == 200
    assert response.json() == {
        "result": (
            "Player X made a move at (1, 1)\n"
            "Player O made a move at (2, 1)\n"
            "X|X|O\n"
            "O|X|.\n"
            ".|O|."
        )
    }

    response = client.post(f"/games/{game_id}/move/", json={"x": 2, "y": 2})
    assert response.status_code == 200
    assert response.json() == {
        "result": (
            "Player X made a move at (2, 2)\n" "Player X wins!\n" "X|X|O\n" "O|X|.\n" ".|O|X"
        )
    }

    response = client.post(f"/games/{game_id}/move/", json={"x": 2, "y": 1})
    assert response.status_code == 200
    assert "Game is already over." in response.text


def test_get_game(client):
    response = client.post("/games/")
    game_id = response.json()
    response = client.get(f"/games/{game_id}/")
    assert response.status_code == 200
    assert response.json() == {
        "id": game_id,
        "board": [[".", ".", "."], [".", ".", "."], [".", ".", "."]],
        "current_player": "X",
        "winner": None,
        "available_moves": [
            [0, 0],
            [0, 1],
            [0, 2],
            [1, 0],
            [1, 1],
            [1, 2],
            [2, 0],
            [2, 1],
            [2, 2],
        ],
        "moves": [],
    }


def test_get_games(client):
    response = client.post("/games/")
    game_id = response.json()
    response = client.get("/games/")
    assert response.status_code == 200
    assert game_id in response.json()


def test_get_game_moves(client):
    response = client.post("/games/")
    game_id = response.json()
    response = client.get(f"/games/{game_id}/moves/")
    assert response.status_code == 200
    assert response.json() == []

    response = client.post(f"/games/{game_id}/move/", json={"x": 0, "y": 0})
    response = client.get(f"/games/{game_id}/moves/")
    assert response.status_code == 200
    assert response.json() == [[0, 0], [1, 1]]

    response = client.post(f"/games/{game_id}/move/", json={"x": 0, "y": 2})
    response = client.get(f"/games/{game_id}/moves/")
    assert response.status_code == 200
    assert response.json() == [[0, 0], [1, 1], [0, 2], [1, 0]]


def test_get_game_replay(client):
    response = client.post("/games/")
    game_id = response.json()
    response = client.get(f"/games/{game_id}/replay/")
    assert response.status_code == 200
    assert response.json() == {'result': ''}

    response = client.post(f"/games/{game_id}/move/", json={"x": 0, "y": 0})
    response = client.get(f"/games/{game_id}/replay/")
    assert response.status_code == 200
    assert "X played at (0, 0)" in response.json()["result"]
