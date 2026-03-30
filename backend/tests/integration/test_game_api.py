import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_user_repo, get_session_repo, get_transcript_provider, get_llm_orchestrator
from unittest.mock import AsyncMock, MagicMock
from app.domain.schemas import PlayerProfile, GameSession, EnemyState, QuestionSchema, OptionSchema

client = TestClient(app)

# --- Mocks for Integration ---

@pytest.fixture
def mock_user_repo():
    return AsyncMock()

@pytest.fixture
def mock_session_repo():
    return AsyncMock()

@pytest.fixture
def mock_transcript_provider():
    return AsyncMock()

@pytest.fixture
def mock_llm_orchestrator():
    return AsyncMock()

# --- E2E Smoke Test ---

def test_api_game_flow_full_sequence(
    mock_user_repo,
    mock_session_repo,
    mock_transcript_provider,
    mock_llm_orchestrator
):
    """
    Verifica que el flujo completo de la API esté bien cableado:
    POST /game/start -> POST /game/play
    Usamos dependency_overrides para inyectar los mocks en FastAPI.
    """
    
    # 1. Preparar overrides de FastAPI
    app.dependency_overrides[get_user_repo] = lambda: mock_user_repo
    app.dependency_overrides[get_session_repo] = lambda: mock_session_repo
    app.dependency_overrides[get_transcript_provider] = lambda: mock_transcript_provider
    app.dependency_overrides[get_llm_orchestrator] = lambda: mock_llm_orchestrator

    # 2. Mock Data
    video_id = "youtube_123"
    user_id = "test_user"
    email = "test@example.com"
    
    # Mocking Start Game returns
    mock_user_repo.get_user.return_value = None
    mock_transcript_provider.get_transcript.return_value = "Video transcript"
    
    initial_q = QuestionSchema(
        enemy_name="Bug Lord",
        question_text="What is TDD?",
        options=[OptionSchema(id=0, text="Test"), OptionSchema(id=1, text="Code")],
        correct_option_id=0,
        explanation="Tests first"
    )
    mock_llm_orchestrator.generate_question.return_value = initial_q

    # 3. Test /game/start
    start_payload = {"user_id": user_id, "email": email, "video_id": video_id}
    response = client.post("/api/v1/game/start", json=start_payload)
    
    assert response.status_code == 200
    session_data = response.json()
    session_id = session_data["session_id"]
    assert session_data["enemy"]["name"] == "Bug Lord"
    assert session_data["current_question"]["question_text"] == "What is TDD?"

    # 4. Mocking Play Turn (Next turn)
    # Re-mocking for the session lookup
    current_session = GameSession(**session_data)
    mock_session_repo.get_session.return_value = current_session
    mock_user_repo.get_user.return_value = PlayerProfile(user_id=user_id, email=email, character_path="x")
    
    next_q = QuestionSchema(
        question_text="Next Q?",
        options=[OptionSchema(id=0, text="A"), OptionSchema(id=1, text="B")],
        correct_option_id=1,
        explanation="Explanation"
    )
    mock_llm_orchestrator.generate_question.return_value = next_q

    # 5. Test /game/play
    play_payload = {"session_id": session_id, "answer_index": 0} # Correct answer
    response = client.post("/api/v1/game/play", json=play_payload)

    assert response.status_code == 200
    play_result = response.json()
    assert play_result["is_correct"] is True
    assert play_result["damage_dealt"] == 25
    assert play_result["next_question"]["question_text"] == "Next Q?"

    # Limpiar overrides
    app.dependency_overrides.clear()
