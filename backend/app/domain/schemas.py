from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

# --- 1. AI BRAIN SCHEMAS (LLM Structured Output) ---

class OptionSchema(BaseModel):
    id: int
    text: str

class QuestionSchema(BaseModel):
    question_text: str
    options: List[OptionSchema] = Field(..., min_length=2, max_length=5)
    correct_option_id: int
    explanation: str
    
    # Extra field for logic but not always part of the LLM JSON? 
    # Actually, GeminiAdapter adds it.
    enemy_name: Optional[str] = None 

class QuestionGenerationContext(BaseModel):
    video_id: str
    transcript_chunk: str
    player_level: int
    topic_focus: str

# --- 2. USER & GAME STATE SCHEMAS (Database mapping) ---

class PlayerProfile(BaseModel):
    user_id: str = Field(..., description="The unique Firebase Auth UID")
    email: EmailStr
    username: Optional[str] = None
    character_path: str = Field(..., description="Chosen character path")
    
    current_hp: int = Field(default=100, ge=0)
    max_hp: int = Field(default=100, ge=1)
    level: int = Field(default=1, ge=1)
    xp: int = Field(default=0, ge=0)
    
    skills: List[str] = Field(default_factory=list)
    unlocked_nodes: List[str] = Field(default_factory=list)

class EnemyState(BaseModel):
    name: str
    max_hp: int = Field(default=50, ge=1)
    current_hp: int = Field(default=50, ge=0)
    topic: str

class GameSession(BaseModel):
    session_id: str = Field(..., description="Unique ID for the game session")
    user_id: str
    video_id: str
    enemy: EnemyState
    current_question: Optional[QuestionSchema] = None
    is_active: bool = True
    created_at: str = Field(default_factory=lambda: "2026-03-20T12:00:00Z")

class PlayTurnResult(BaseModel):
    is_correct: bool
    damage_dealt: int
    damage_taken: int
    player_hp: int
    enemy_hp: int
    next_question: Optional[QuestionSchema] = None
    combat_log: str
    is_session_active: bool
