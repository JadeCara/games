import pytest
from games.tic_tac_toe import TicTacToe


def vertical_moves():
    return [
        ((1, 1), None),
        ((0, 2), None),
        ((0, 1), None),
        ((1, 0), None),
        ((2, 1), "X"),
        ((1, 2), "ERR"),
    ]


def horizontal_moves():
    return [
        ((1, 1), None),
        ((0, 2), None),
        ((1, 0), None),
        ((0, 1), None),
        ((1, 2), "X"),
        ((1, 2), "ERR"),
    ]


def diagonal_moves():
    return [
        ((1, 1), None),
        ((0, 2), None),
        ((0, 0), None),
        ((1, 0), None),
        ((2, 2), "X"),
        ((1, 2), "ERR"),
    ]


@pytest.fixture
def game():
    return TicTacToe("1")


@pytest.fixture
def moves(request):
    if request.param == "vertical_moves":
        return vertical_moves()
    if request.param == "horizontal_moves":
        return horizontal_moves()
    if request.param == "diagonal_moves":
        return diagonal_moves()


def test_new_game():
    game = TicTacToe("1")
    assert game.board == [["." for _ in range(3)] for _ in range(3)]
    assert game.current_player == "X"
    assert game.available_moves == [(i, j) for i in range(3) for j in range(3)]
    assert game.moves == []
    assert game.render_board()


def test_is_valid_move(game):
    assert game.is_valid_move(0, 0)
    assert game.is_valid_move(2, 2)
    assert not game.is_valid_move(-1, 0)
    assert not game.is_valid_move(0, 3)
    game.board[0][0] = "X"
    assert not game.is_valid_move(0, 0)


def test_check_winner(game):
    assert game.check_winner() is None
    # Horizontal wins
    game.board = [["X", "X", "X"], [".", ".", "."], [".", ".", "."]]
    assert game.check_winner() == "X"
    game.board = [[".", ".", "."], ["X", "X", "X"], [".", ".", "."]]
    assert game.check_winner() == "X"
    game.board = [[".", ".", "."], [".", ".", "."], ["X", "X", "X"]]
    assert game.check_winner() == "X"
    # Vertical wins
    game.board = [["X", ".", "."], ["X", ".", "."], ["X", ".", "."]]
    assert game.check_winner() == "X"
    game.board = [[".", "X", "."], [".", "X", "."], [".", "X", "."]]
    assert game.check_winner() == "X"
    game.board = [[".", ".", "X"], [".", ".", "X"], [".", ".", "X"]]
    assert game.check_winner() == "X"
    # Diagonal wins
    game.board = [["X", ".", "."], [".", "X", "."], [".", ".", "X"]]
    assert game.check_winner() == "X"
    game.board = [[".", ".", "X"], [".", "X", "."], ["X", ".", "."]]
    assert game.check_winner() == "X"
    # Draw
    game.board = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]
    assert game.check_winner() is None


@pytest.mark.parametrize(
    "moves", ["vertical_moves", "horizontal_moves", "diagonal_moves"], indirect=True
)
def test_make_move(moves, game):
    for move in moves:
        winner = move[1]
        current_player = game.current_player
        if winner == "ERR":
            assert game.make_move(move[0][0], move[0][1]) == "Game is already over."
        else:
            game.make_move(move[0][0], move[0][1])
            assert game.render_board()
            assert move[0] not in game.available_moves
            assert move[0] in game.moves
            if winner is None:
                assert game.check_winner() is None
                assert game.current_player != current_player
                assert len(game.available_moves) == 9 - len(game.moves)
            else:
                assert game.check_winner() == winner
                assert game.available_moves == {}


def test_replay(game):
    game.moves = [(0, 0), (0, 1), (1, 1), (0, 2), (2, 2)]
    game.winner = "X"
    assert game.replay() == (
        "X played at (0, 0)\n"
        "X|.|.\n"
        ".|.|.\n"
        ".|.|.\n"
        "O played at (0, 1)\n"
        "X|O|.\n"
        ".|.|.\n"
        ".|.|.\n"
        "X played at (1, 1)\n"
        "X|O|.\n"
        ".|X|.\n"
        ".|.|.\n"
        "O played at (0, 2)\n"
        "X|O|O\n"
        ".|X|.\n"
        ".|.|.\n"
        "X played at (2, 2)\n"
        "X|O|O\n"
        ".|X|.\n"
        ".|.|X\n"
        "Player X wins!"
    )
