from typing import Optional
from app.domain.schemas import GameSession, PlayTurnResult, QuestionGenerationContext
from app.domain.battle import evaluate_answer, Player, Enemy
from app.application.ports.database_repository import IUserRepository, IGameSessionRepository
from app.application.ports.llm_orchestrator import ILLMOrchestrator
from app.application.ports.video_transcript_provider import VideoTranscriptProvider

class PlayTurnUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        session_repo: IGameSessionRepository,
        llm_orchestrator: ILLMOrchestrator,
        transcript_provider: VideoTranscriptProvider
    ):
        self.user_repo = user_repo
        self.session_repo = session_repo
        self.llm_orchestrator = llm_orchestrator
        self.transcript_provider = transcript_provider

    async def execute(self, session_id: str, chosen_index: int) -> PlayTurnResult:
        # 1. Obtener la sesión
        session = await self.session_repo.get_session(session_id)
        if not session or not session.is_active:
            raise ValueError("Sesión no encontrada o ya finalizada.")

        # 2. Obtener el jugador
        player_profile = await self.user_repo.get_user(session.user_id)
        if not player_profile:
            raise ValueError("Jugador no encontrado.")

        # 3. Preparar modelos de dominio para la lógica de combate
        domain_player = Player(hp=player_profile.current_hp)
        domain_enemy = Enemy(hp=session.enemy.current_hp)
        
        # 4. Validar respuesta y aplicar daño
        correct_index = session.current_question.correct_option_id
        is_correct = (correct_index == chosen_index)
        
        damage = 25 # Daño base fijo
        
        previous_player_hp = domain_player.hp
        previous_enemy_hp = domain_enemy.hp
        
        evaluate_answer(domain_player, domain_enemy, correct_index, chosen_index, damage)
        
        damage_dealt = previous_enemy_hp - domain_enemy.hp
        damage_taken = previous_player_hp - domain_player.hp

        # 5. Combat Log
        if is_correct:
            combat_log = f"¡Correcto! Dañaste a {session.enemy.name} por {damage_dealt} HP."
        else:
            combat_log = f"¡Fallaste! {session.enemy.name} te infligió {damage_taken} HP."

        # 6. Actualizar perfiles y sesión
        player_profile.current_hp = max(0, domain_player.hp)
        session.enemy.current_hp = max(0, domain_enemy.hp)
        
        next_question = None
        is_session_active = True
        
        if player_profile.current_hp <= 0:
            combat_log += " HAS MUERTO."
            is_session_active = False
            session.is_active = False
        elif session.enemy.current_hp <= 0:
            combat_log += f" ¡{session.enemy.name} ha sido derrotado!"
            is_session_active = False
            session.is_active = False
        else:
            # Pedir nueva pregunta
            transcript = await self.transcript_provider.get_transcript(session.video_id)
            context = QuestionGenerationContext(
                video_id=session.video_id,
                transcript_chunk=transcript[:5000],
                player_level=player_profile.level,
                topic_focus="Gameplay progression"
            )
            next_question = await self.llm_orchestrator.generate_question(context)
            session.current_question = next_question

        # 7. Guardar cambios
        await self.user_repo.save_user(player_profile)
        await self.session_repo.save_session(session)

        return PlayTurnResult(
            is_correct=is_correct,
            damage_dealt=damage_dealt,
            damage_taken=damage_taken,
            player_hp=player_profile.current_hp,
            enemy_hp=session.enemy.current_hp,
            next_question=next_question,
            combat_log=combat_log,
            is_session_active=is_session_active
        )
