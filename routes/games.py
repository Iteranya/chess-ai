# Manager to hold games in memory (you could swap this with Redis or a DB)
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.chess import ChessGame

game_store = {}

# FastAPI app
router = APIRouter(
    prefix="/game",
    tags=["Chess Game"]
)

class StartGameRequest(BaseModel):
    player_color: str = 'white'
    player_elo: int = 1200
    computer_elo: int = 1500

class MoveRequest(BaseModel):
    move_uci: str

@router.post("/start")
def start_game(req: StartGameRequest):
    game_id = str(uuid.uuid4())
    game = ChessGame(req.player_color, req.player_elo, req.computer_elo)
    game_store[game_id] = game
    return {"game_id": game_id, "board": game.get_board_fen()}

@router.post("/move/{game_id}")
def make_move(game_id: str, req: MoveRequest):
    if game_id not in game_store:
        raise HTTPException(status_code=404, detail="Game not found")

    game = game_store[game_id]
    try:
        game.player_move(req.move_uci)
        comp_move = game.computer_move()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "player_move": req.move_uci,
        "computer_move": comp_move,
        "board": game.get_board_fen(),
        "game_over": game.is_game_over(),
        "result": game.get_result()
    }

@router.get("/status/{game_id}")
def get_status(game_id: str):
    if game_id not in game_store:
        raise HTTPException(status_code=404, detail="Game not found")

    game = game_store[game_id]
    return {
        "board": game.get_board_fen(),
        "game_over": game.is_game_over(),
        "result": game.get_result()
    }

@router.post("/end/{game_id}")
def end_game(game_id: str):
    if game_id in game_store:
        game_store[game_id].close()
        del game_store[game_id]
        return {"message": "Game ended and resources cleaned up."}
    else:
        raise HTTPException(status_code=404, detail="Game not found")