import pytest
from unittest.mock import AsyncMock, MagicMock
from app.application.use_cases.start_game import StartGameUseCase
from app.domain.schemas import PlayerProfile, QuestionSchema, GameSession

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

@pytest.mark.asyncio
async def test_start_game_success(
    mock_user_repo,
    mock_session_repo,
    mock_transcript_provider,
    mock_llm_orchestrator
):
    # Setup
    user_id = "user_123"
    email = "test@example.com"
    video_id = "vid_abc"
    transcript = "This is a video script about coding."
    
    # Mock behavior
    mock_user_repo.get_user.return_value = None # New player
    mock_transcript_provider.get_transcript.return_value = transcript
    
    mock_question = QuestionSchema(
        enemy_name="Bug Lord",
        question_text="What is a unit test?",
        options=[
            {"id": 0, "text": "A bug"},
            {"id": 1, "text": "A small test"},
            {"id": 2, "text": "A video"},
            {"id": 3, "text": "Nothing"}
        ],
        correct_option_id=1,
        explanation="Tests small units of code."
    )
    mock_llm_orchestrator.generate_question.return_value = mock_question

    # Use Case
    use_case = StartGameUseCase(
        user_repo=mock_user_repo,
        session_repo=mock_session_repo,
        transcript_provider=mock_transcript_provider,
        llm_orchestrator=mock_llm_orchestrator
    )

    session = await use_case.execute(user_id, email, video_id)

    # Verifications
    assert session.user_id == user_id
    assert session.video_id == video_id
    assert session.enemy.name == "Bug Lord"
    assert session.current_question.question_text == "What is a unit test?"
    assert session.is_active is True
    
    # Verify collaborative calls
    mock_user_repo.get_user.assert_called_once_with(user_id)
    mock_user_repo.save_user.assert_called_once()
    mock_transcript_provider.get_transcript.assert_called_once_with(video_id)
    mock_llm_orchestrator.generate_question.assert_called_once_with(transcript)
    mock_session_repo.save_session.assert_called_once()
