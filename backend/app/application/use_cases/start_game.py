import uuid
from typing import Optional
from app.domain.schemas import PlayerProfile, GameSession, EnemyState, QuestionGenerationContext
from app.application.ports.database_repository import IUserRepository, IGameSessionRepository
from app.application.ports.video_transcript_provider import VideoTranscriptProvider
from app.application.ports.llm_orchestrator import ILLMOrchestrator

class StartGameUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        session_repo: IGameSessionRepository,
        transcript_provider: VideoTranscriptProvider,
        llm_orchestrator: ILLMOrchestrator
    ):
        self.user_repo = user_repo
        self.session_repo = session_repo
        self.transcript_provider = transcript_provider
        self.llm_orchestrator = llm_orchestrator

    async def execute(self, user_id: str, email: str, video_id: str) -> GameSession:
        # 1. Obtener o crear el perfil del jugador
        player = await self.user_repo.get_user(user_id)
        if not player:
            player = PlayerProfile(
                user_id=user_id,
                email=email,
                character_path="backend_knight", # Senda por defecto
                current_hp=100,
                max_hp=100,
                level=1
            )
            await self.user_repo.save_user(player)

        # 2. Obtener el transcript del video de YouTube
        transcript = await self.transcript_provider.get_transcript(video_id)

        # 3. Generar el primer enemigo y pregunta usando Gemini
        context = QuestionGenerationContext(
            video_id=video_id,
            transcript_chunk=transcript[:5000], # Tomamos un trozo manejable
            player_level=player.level,
            topic_focus="General concepts"
        )
        question_data = await self.llm_orchestrator.generate_question(context)

        # 4. Crear el estado del enemigo inicial
        enemy = EnemyState(
            name=question_data.enemy_name or "Bug Lord",
            max_hp=50,
            current_hp=50,
            topic="General AI/Code"
        )

        # 5. Crear la sesión de juego
        session = GameSession(
            session_id=str(uuid.uuid4()),
            user_id=user_id,
            video_id=video_id,
            enemy=enemy,
            current_question=question_data,
            is_active=True
        )

        # 6. Persistir la sesión
        await self.session_repo.save_session(session)

        return session
