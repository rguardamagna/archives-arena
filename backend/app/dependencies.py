import os
from fastapi import Depends
from app.infrastructure.adapters.firestore_repository import FirestoreUserRepository
from app.infrastructure.adapters.youtube_adapter import YoutubeTranscriptAdapter
from app.infrastructure.adapters.gemini_adapter import GeminiAdapter
from app.application.use_cases.start_game import StartGameUseCase
from app.application.use_cases.play_turn import PlayTurnUseCase

# --- Singleton Adapters (Simulated) ---

def get_user_repo():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    return FirestoreUserRepository(project_id=project_id)

def get_session_repo():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    return FirestoreUserRepository(project_id=project_id)

def get_transcript_provider():
    return YoutubeTranscriptAdapter()

def get_llm_orchestrator():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY no configurada en el entorno.")
    return GeminiAdapter() # El adaptador ya lee del entorno o usa el default

# --- Use Case Factory Dependencies ---

def get_start_game_use_case(
    user_repo=Depends(get_user_repo),
    session_repo=Depends(get_session_repo),
    transcript_provider=Depends(get_transcript_provider),
    llm_orchestrator=Depends(get_llm_orchestrator)
):
    return StartGameUseCase(user_repo, session_repo, transcript_provider, llm_orchestrator)

def get_play_turn_use_case(
    user_repo=Depends(get_user_repo),
    session_repo=Depends(get_session_repo),
    transcript_provider=Depends(get_transcript_provider),
    llm_orchestrator=Depends(get_llm_orchestrator)
):
    return PlayTurnUseCase(user_repo, session_repo, llm_orchestrator, transcript_provider)
