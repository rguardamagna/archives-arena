# 🧠 Spec: The AI Brain (Question Generator)

> **Document Status:** DRAFT | **Phase:** Planning | **Target:** LLM Integration

## 1. Overview
The AI Brain is responsible for interrupting the YouTube video at specific intervals, reading the recent chunk of subtitles (transcript), and generating a dynamic, context-aware Multiple Choice Question (MCQ). 

This operation **must** return a perfectly structured JSON object so our FastAPI endpoints can parse it, validate it, and send it to the Frontend without breaking the game loop.

---

## 2. The Data Contracts (Pydantic Mocks)

Before writing any Python code, these are the strict schemas the Agent (`[Implementer]`) will use to guarantee type safety.

### 2.1 The Input Payload
When the App calls the LLM, it sends this Context:
```python
class QuestionGenerationContext(BaseModel):
    video_id: str
    transcript_chunk: str  # The actual text spoken in the video
    player_level: int      # To adjust the difficulty of the question
    topic_focus: str       # E.g., "Python decorators", "Memory management"
```

### 2.2 The Output Schema (Enforced JSON)
The LLM **MUST** return this exact structure:
```python
class OptionSchema(BaseModel):
    id: int
    text: str

class QuestionSchema(BaseModel):
    question_text: str
    options: list[OptionSchema]  # Exactly 4 options
    correct_option_id: int       # The ID of the correct answer
    explanation: str             # To show the player AFTER they answer (learning loop)
```

---

## 3. The System Prompt (The Rules of Engagement)

The Agent designing the final prompt must ensure these boundaries:
1. **Persona:** "You are an expert game designer and educator."
2. **Constraint 1 (No Hallucinations):** The question MUST be based *exclusively* on the `transcript_chunk`. If the video says X, the answer is X.
3. **Constraint 2 (Distractors):** The wrong options must be highly plausible to a novice, not obvious fake answers.
4. **Constraint 3 (JSON Only):** No markdown backticks, no introductory text ("Sure, here is your json:"). Just raw stringified JSON matching `QuestionSchema`.

---

## 4. The Hexagonal Port (Interface)
```python
class ILLMQuestionGenerator(Protocol):
    async def generate_question(self, context: QuestionGenerationContext) -> QuestionSchema:
        ...
```
*Note: Any Agent implementing this Port must ensure it catches `ValidationError` from Pydantic and triggers a retry logic if the LLM fails the schema.*
