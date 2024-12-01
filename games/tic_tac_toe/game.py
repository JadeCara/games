import random
from pydantic import BaseModel, Field


class TicTacToe(BaseModel):
    """
    Tic Tac Toe game class.
    Keeps track of whose turn it is.
    Keeps track of the board state.
    Makes Computer moves.

    """

    id: str
    board: list[list[str]] = Field(
        default_factory=lambda: [["." for _ in range(3)] for _ in range(3)]
    )
    current_player: str = "X"
    available_moves: set[tuple[int, int]] = Field(
        default_factory=lambda: sorted({(x, y) for x in range(3) for y in range(3)})
    )
    moves: list[tuple[int, int]] = Field(default_factory=list)
    winner: str = None

    def __init__(self, game_id: str, **data):
        super().__init__(id=game_id, **data)

    def is_valid_move(self, x: int, y: int):
        """Check if the move is valid."""
        return (
            0 <= x < 3 and 0 <= y < 3 and self.board[x][y] == "." and (x, y) in self.available_moves
        )

    def computer_move(self):
        """Make a random move for the computer."""
        move = random.choice(list(self.available_moves))
        return self.make_move(move[0], move[1])

    def make_move(self, x: int, y: int):
        """Make a move on the board."""
        if len(self.available_moves) == 0:
            return "Game is already over."
        if not self.is_valid_move(x, y):
            return f"Invalid move: ({x}, {y})"
        self.board[x][y] = self.current_player
        self.moves.append((x, y))
        self.winner = self.check_winner()
        if self.winner is not None:
            self.available_moves = {}
            message = [
                f"Player {self.current_player} made a move at ({x}, {y})",
                f"Player {self.winner} wins!",
            ]
            return "\n".join(message)
        if not self.available_moves:
            self.winner = "DRAW"
            return "Game is a draw!"
        self.available_moves.remove((x, y))
        current_player = self.current_player
        self.current_player = "O" if self.current_player == "X" else "X"
        return f"Player {current_player} made a move at ({x}, {y})"

    def check_winner(self):
        """Check if there is a winner."""
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ".":
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ".":
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ".":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ".":
            return self.board[0][2]
        return None

    def render_board(self):
        return "\n".join(["|".join(row) for row in self.board])

    def replay(self):
        """Renders the board for each move in the game."""
        replay_board = [["." for _ in range(3)] for _ in range(3)]
        replay_player = "X"
        replay = []
        for move in self.moves:
            x = move[0]
            y = move[1]
            replay.append(f"{replay_player} played at ({x}, {y})")
            replay_board[x][y] = replay_player
            replay_player = "X" if replay_player == "O" else "O"
            replay.append("\n".join(["|".join(row) for row in replay_board]))
        if self.winner is not None:
            replay.append(f"Player {self.winner} wins!")
        return "\n".join(replay)
