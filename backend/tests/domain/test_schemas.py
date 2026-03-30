import pytest
from pydantic import ValidationError
from app.domain.schemas import PlayerProfile, QuestionSchema, OptionSchema

def test_player_profile_valid():
    player = PlayerProfile(
        user_id="firebase_abc123",
        email="darkknight@tuberpg.com",
        character_path="backend_knight"
    )
    assert player.current_hp == 100
    assert player.level == 1
    assert player.skills == []

def test_player_profile_invalid_email():
    with pytest.raises(ValidationError):
        PlayerProfile(
            user_id="firebase_abc123",
            email="not-an-email",
            character_path="backend_knight"
        )

def test_question_schema_valid():
    q = QuestionSchema(
        question_text="What is a Docker container?",
        options=[
            OptionSchema(id=1, text="A lightweight VM"),
            OptionSchema(id=2, text="A plastic box"),
            OptionSchema(id=3, text="A database")
        ],
        correct_option_id=1,
        explanation="It isolates processes."
    )
    assert len(q.options) == 3

def test_question_schema_invalid_options_length():
    # Pydantic should catch if we supply fewer than 2 options
    with pytest.raises(ValidationError):
        QuestionSchema(
            question_text="Too few options?",
            options=[OptionSchema(id=1, text="Yes")],
            correct_option_id=1,
            explanation="Needs at least 2."
        )
