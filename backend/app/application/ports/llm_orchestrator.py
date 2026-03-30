from typing import Protocol
from app.domain.schemas import QuestionGenerationContext, QuestionSchema

class ILLMOrchestrator(Protocol):
    async def generate_question(self, context: QuestionGenerationContext) -> QuestionSchema:
        """
        Generates a strictly validated JSON question based on the provided video context.
        """
        ...
