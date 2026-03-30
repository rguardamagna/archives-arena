import pytest
from unittest.mock import AsyncMock, MagicMock
from app.application.use_cases.play_turn import PlayTurnUseCase
from app.domain.schemas import PlayerProfile, GameSession, EnemyState, QuestionSchema, OptionSchema

@pytest.fixture
def mock_user_repo():
    return AsyncMock()

@pytest.fixture
def mock_session_repo():
    return AsyncMock()

@pytest.fixture
def mock_llm_orchestrator():
    return AsyncMock()

@pytest.fixture
def mock_transcript_provider():
    return AsyncMock()

@pytest.mark.asyncio
async def test_play_turn_correct_answer(
    mock_user_repo,
    mock_session_repo,
    mock_llm_orchestrator,
    mock_transcript_provider
):
    # Setup
    session_id = "sess_123"
    player = PlayerProfile(user_id="u1", email="t@t.com", character_path="warrior", current_hp=100, max_hp=100)
    
    current_q = QuestionSchema(
        question_text="Q1",
        options=[OptionSchema(id=0, text="A"), OptionSchema(id=1, text="B")],
        correct_option_id=0,
        explanation="X"
    )
    
    enemy = EnemyState(name="E1", max_hp=50, current_hp=50, topic="T")
    session = GameSession(session_id=session_id, user_id="u1", video_id="v1", enemy=enemy, current_question=current_q)

    # Mock behavior
    mock_session_repo.get_session.return_value = session
    mock_user_repo.get_user.return_value = player
    
    next_q = QuestionSchema(
        question_text="Q2",
        options=[OptionSchema(id=0, text="C"), OptionSchema(id=1, text="D")],
        correct_option_id=0,
        explanation="Y"
    )
    mock_llm_orchestrator.generate_question.return_value = next_q
    mock_transcript_provider.get_transcript.return_value = "transcript"

    # Use Case
    use_case = PlayTurnUseCase(mock_user_repo, mock_session_repo, mock_llm_orchestrator, mock_transcript_provider)
    result = await use_case.execute(session_id, chosen_index=0)

    # Verifications
    assert result.is_correct is True
    assert result.damage_dealt == 20
    assert result.enemy_hp == 30
    assert result.next_question == next_q
    mock_session_repo.save_session.assert_called_once()
    mock_user_repo.save_user.assert_called_once()

@pytest.mark.asyncio
async def test_play_turn_wrong_answer(
    mock_user_repo,
    mock_session_repo,
    mock_llm_orchestrator,
    mock_transcript_provider
):
    # Setup
    session_id = "sess_123"
    player = PlayerProfile(user_id="u1", email="t@t.com", character_path="warrior", current_hp=100, max_hp=100)
    current_q = QuestionSchema(
        question_text="Q1",
        options=[OptionSchema(id=0, text="A"), OptionSchema(id=1, text="B")],
        correct_option_id=0,
        explanation="X"
    )
    enemy = EnemyState(name="E1", max_hp=50, current_hp=50, topic="T")
    session = GameSession(session_id=session_id, user_id="u1", video_id="v1", enemy=enemy, current_question=current_q)

    mock_session_repo.get_session.return_value = session
    mock_user_repo.get_user.return_value = player
    mock_llm_orchestrator.generate_question.return_value = current_q # actually next q
    mock_transcript_provider.get_transcript.return_value = "transcript"

    # Use Case (Incorrect answer: 1 instead of 0)
    use_case = PlayTurnUseCase(mock_user_repo, mock_session_repo, mock_llm_orchestrator, mock_transcript_provider)
    result = await use_case.execute(session_id, chosen_index=1)

    # Verifications
    assert result.is_correct is False
    assert result.damage_taken == 20
    assert result.player_hp == 80
    assert result.enemy_hp == 50
