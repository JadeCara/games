from pydantic import BaseModel, Field

from games.tic_tac_toe import TicTacToe


class GameContext(BaseModel):
    """
    The GameContext class is responsible for managing the games.
    It creates games, makes moves, and retrieves game information for multiple games.
    """

    games: dict[str, TicTacToe] = Field(default_factory=dict)

    def create_game(self):
        """Create a new game and return the game id."""
        game_id = str(len(self.games))
        self.games[game_id] = TicTacToe(game_id)
        return game_id

    def make_move(self, game_id, x, y):
        """
        Make a move in the game.
        This will also call the computer_move method to make a move for the computer.
        """
        result = []
        game_id = game_id.replace('"', "")
        game = self.games[game_id]
        player_move = game.make_move(x, y)

        if "Invalid move" in player_move:
            return player_move

        if "over" in player_move:
            return player_move

        result.append(player_move)

        if "wins" in player_move or "draw" in player_move:
            result.append(self.games[game_id].render_board())
            return "\n".join(result)

        result.append(self.games[game_id].computer_move())
        result.append(self.games[game_id].render_board())

        return "\n".join(result)

    def get_game(self, game_id):
        return self.games[game_id]

    def get_games(self):
        return {
            game_id: {
                "winner": self.games[game_id].winner,
                "move_count": len(self.games[game_id].moves),
            }
            for game_id in self.games
        }

    def get_game_moves(self, game_id):
        return self.games[game_id].moves

    def get_game_replay(self, game_id):
        return self.games[game_id.replace("'", "")].replay()
