from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, field_validator
from games.game_context import GameContext

app = FastAPI()
game_context = GameContext()

# Serve the static files
app.mount("/static", StaticFiles(directory="static"), name="static")


class Move(BaseModel):
    x: int
    y: int

    @field_validator("x", "y")
    def check_coordinates(cls, value):
        if value < 0 or value >= 3:
            raise ValueError("Coordinates must be between 0 and 2 inclusive")
        return value


@app.post("/games/")
def create_game():
    game_id = game_context.create_game()
    return game_id


@app.post("/games/{game_id}/move/")
def make_move(game_id: str, move: Move):
    try:
        result = game_context.make_move(game_id, move.x, move.y)
        return {"result": result}
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/games/{game_id}/")
def get_game(game_id: str):
    try:
        game = game_context.get_game(game_id)
        return game
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not found")


@app.get("/games/")
def get_games():
    return game_context.get_games()


@app.get("/games/{game_id}/moves/")
def get_game_moves(game_id: str):
    try:
        return game_context.get_game_moves(game_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not found")


@app.get("/games/{game_id}/replay/")
def get_game_replay(game_id: str):
    try:
        return {"result": game_context.get_game_replay(game_id)}
    except KeyError:
        raise HTTPException(status_code=404, detail="Game not found")


# Serve the index.html file
@app.get("/")
def read_root():
    return FileResponse("static/index.html")
