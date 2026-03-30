import json
import os
from pydantic import ValidationError
from google import genai
from google.genai import types

from app.application.ports.llm_orchestrator import ILLMOrchestrator
from app.domain.schemas import QuestionGenerationContext, QuestionSchema

# --- System Prompt (The Rules of Engagement as defined in spec_ai_brain.md) ---
SYSTEM_PROMPT = """You are an expert game designer and educator.
Your task is to create a Multiple Choice Question (MCQ) for an educational RPG game.

STRICT RULES:
1. The question MUST be based EXCLUSIVELY on the provided transcript text. Do NOT use external knowledge.
2. The wrong options (distractors) MUST be highly plausible to a novice, not obviously fake.
3. You MUST respond with ONLY a raw JSON object. No markdown, no backticks, no introductory text.

The JSON must match this exact structure:
{
  "question_text": "string",
  "options": [
    {"id": 1, "text": "string"},
    {"id": 2, "text": "string"},
    {"id": 3, "text": "string"},
    {"id": 4, "text": "string"}
  ],
  "correct_option_id": 1,
  "explanation": "string"
}"""

MAX_RETRIES = 3


class GeminiAdapter(ILLMOrchestrator):
    """
    Infrastructure Adapter for Google Gemini (google.genai SDK).
    Implements ILLMOrchestrator to generate structured MCQ questions.
    Uses retry logic to handle LLM schema failures gracefully.
    """

    def __init__(self, model_name: str = "gemini-flash-lite-latest"):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name

    async def generate_question(self, context: QuestionGenerationContext) -> QuestionSchema:
        """
        Generates a validated QuestionSchema from a video transcript chunk.
        Retries up to MAX_RETRIES times if the LLM returns malformed JSON.
        """
        user_prompt = f"""
Player Level: {context.player_level}
Topic Focus: {context.topic_focus}

Transcript to evaluate:
---
{context.transcript_chunk}
---

Generate one MCQ question based strictly on the transcript above.
"""
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
        )

        for attempt in range(1, MAX_RETRIES + 1):
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=user_prompt,
                config=config,
            )
            raw_text = response.text.strip()

            try:
                data = json.loads(raw_text)
                return QuestionSchema(**data)
            except (json.JSONDecodeError, ValidationError) as e:
                if attempt == MAX_RETRIES:
                    raise RuntimeError(
                        f"GeminiAdapter failed to produce valid JSON after {MAX_RETRIES} attempts. "
                        f"Last error: {e}. Last response: {raw_text}"
                    ) from e
                # Implicit retry on next loop iteration
