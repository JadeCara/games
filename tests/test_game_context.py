import pytest
import random
from games.game_context import GameContext

random.seed(42)


@pytest.fixture
def game_context():
    return GameContext()


def test_game_context_create_game(game_context):
    assert len(game_context.games) == 0
    for _ in range(10):
        game_id = game_context.create_game()
        assert game_id in game_context.games
        assert game_context.games[game_id].id == game_id
    assert len(game_context.games) == 10


def test_game_context_make_move(game_context):
    game_id = game_context.create_game()
    game = game_context.games[game_id]
    assert "Player X made a move at (0, 0)" in game_context.make_move(game_id, 0, 0)
    # Invalid move
    assert "Invalid move: (0, 0)" in game.make_move(0, 0)
    assert "Player X made a move at (2, 0)" in game_context.make_move(game_id, 2, 0)
    assert "Player X made a move at (1, 0)" in game_context.make_move(game_id, 1, 0)
    # Game is over
    assert "Game is already over." in game_context.make_move(game_id, 2, 1)


def test_game_context_get_game(game_context):
    game_id = game_context.create_game()
    game = game_context.get_game(game_id)
    assert game is game_context.games[game_id]


def test_game_context_get_games(game_context):
    game_id = game_context.create_game()
    games = game_context.get_games()
    assert game_id in games
    assert games[game_id]["winner"] is game_context.games[game_id].winner


def test_game_context_get_game_moves(game_context):
    game_id = game_context.create_game()
    print(game_id)
    print(game_context.games.keys())
    game = game_context.games[game_id]
    print(game_id)
    assert game_context.get_game_moves(game_id) == game.moves
