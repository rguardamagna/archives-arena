import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.domain.schemas import QuestionGenerationContext, QuestionSchema
from app.infrastructure.adapters.gemini_adapter import GeminiAdapter

# --- A valid mock response from Gemini ---
VALID_JSON_RESPONSE = json.dumps({
    "question_text": "What is the main purpose of a Docker container?",
    "options": [
        {"id": 1, "text": "To provide process isolation with shared OS kernel"},
        {"id": 2, "text": "To run a full operating system virtually"},
        {"id": 3, "text": "To replace a database server"},
        {"id": 4, "text": "To compile Python code faster"}
    ],
    "correct_option_id": 1,
    "explanation": "Containers share the host OS kernel, unlike VMs which emulate hardware."
})

CONTEXT = QuestionGenerationContext(
    video_id="abc123",
    transcript_chunk="Docker containers provide process isolation while sharing the host OS kernel.",
    player_level=1,
    topic_focus="Containerization"
)


@patch("app.infrastructure.adapters.gemini_adapter.genai")
@patch.dict("os.environ", {"GEMINI_API_KEY": "fake-key-for-testing"})
def test_generate_question_success(mock_genai):
    """Happy path: Gemini returns valid JSON on the first attempt."""
    mock_response = MagicMock()
    mock_response.text = VALID_JSON_RESPONSE

    # The new SDK uses client.aio.models.generate_content (async)
    mock_genai.Client.return_value.aio.models.generate_content = AsyncMock(return_value=mock_response)

    adapter = GeminiAdapter()

    import asyncio
    result = asyncio.run(adapter.generate_question(CONTEXT))

    assert isinstance(result, QuestionSchema)
    assert result.correct_option_id == 1
    assert len(result.options) == 4
    assert "Docker" in result.question_text


@patch("app.infrastructure.adapters.gemini_adapter.genai")
@patch.dict("os.environ", {"GEMINI_API_KEY": "fake-key-for-testing"})
def test_generate_question_retries_on_bad_json(mock_genai):
    """
    Resilience: Gemini returns garbage twice, then valid JSON on the third attempt.
    Applies the retry logic from spec_ai_brain.md (MAX_RETRIES = 3).
    """
    mock_response_bad = MagicMock()
    mock_response_bad.text = "Sure! Here is your question: (malformed)"
    mock_response_good = MagicMock()
    mock_response_good.text = VALID_JSON_RESPONSE

    mock_genai.Client.return_value.aio.models.generate_content = AsyncMock(
        side_effect=[mock_response_bad, mock_response_bad, mock_response_good]
    )

    adapter = GeminiAdapter()

    import asyncio
    result = asyncio.run(adapter.generate_question(CONTEXT))

    assert isinstance(result, QuestionSchema)
    assert mock_genai.Client.return_value.aio.models.generate_content.call_count == 3


@patch("app.infrastructure.adapters.gemini_adapter.genai")
@patch.dict("os.environ", {"GEMINI_API_KEY": "fake-key-for-testing"})
def test_generate_question_raises_after_max_retries(mock_genai):
    """
    Failure mode: Gemini ALWAYS returns garbage. Should raise RuntimeError after MAX_RETRIES.
    """
    mock_response_bad = MagicMock()
    mock_response_bad.text = "I am sorry, I cannot generate that."

    mock_genai.Client.return_value.aio.models.generate_content = AsyncMock(return_value=mock_response_bad)

    adapter = GeminiAdapter()

    import asyncio
    with pytest.raises(RuntimeError, match="GeminiAdapter failed"):
        asyncio.run(adapter.generate_question(CONTEXT))


@patch.dict("os.environ", {}, clear=True)  # Wipe ALL env vars to guarantee no API KEY
def test_adapter_raises_without_api_key():
    """Security: GeminiAdapter must refuse to instantiate without a GEMINI_API_KEY."""
    with pytest.raises(ValueError, match="GEMINI_API_KEY"):
        GeminiAdapter()
