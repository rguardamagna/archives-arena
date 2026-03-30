from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from app.dependencies import get_start_game_use_case, get_play_turn_use_case
from app.application.use_cases.start_game import StartGameUseCase
from app.application.use_cases.play_turn import PlayTurnUseCase
from app.domain.schemas import GameSession, PlayTurnResult

router = APIRouter(prefix="/game", tags=["Game"])

# --- Request Models ---

class StartGameRequest(BaseModel):
    user_id: str
    email: EmailStr
    video_id: str

class PlayTurnRequest(BaseModel):
    session_id: str
    answer_index: int

# --- Endpoints ---

@router.post("/start", response_model=GameSession)
async def start_game(
    request: StartGameRequest,
    use_case: StartGameUseCase = Depends(get_start_game_use_case)
):
    """Inicia una nueva sesión de juego centrada en un video de YouTube."""
    try:
        session = await use_case.execute(
            user_id=request.user_id,
            email=request.email,
            video_id=request.video_id
        )
        return session
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/play", response_model=PlayTurnResult)
async def play_turn(
    request: PlayTurnRequest,
    use_case: PlayTurnUseCase = Depends(get_play_turn_use_case)
):
    """Procesa la respuesta del jugador y calcula el resultado del combate."""
    try:
        result = await use_case.execute(
            session_id=request.session_id,
            chosen_index=request.answer_index
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno procesando el turno.")
