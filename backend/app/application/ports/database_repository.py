from typing import Protocol, Optional
from app.domain.schemas import PlayerProfile, GameSession

class IUserRepository(Protocol):
    async def get_user(self, user_id: str) -> Optional[PlayerProfile]:
        """Fetch a user document by Firebase UID"""
        ...

    async def get_user_by_username(self, username: str) -> Optional[PlayerProfile]:
        """Fetch a user document by its unique username alias"""
        ...
        
    async def save_user(self, user: PlayerProfile) -> None:
        """Upsert a user document into the NoSQL store"""
        ...

class IGameSessionRepository(Protocol):
    async def get_session(self, session_id: str) -> Optional[GameSession]:
        """Fetch a game session by ID"""
        ...
        
    async def save_session(self, session: GameSession) -> None:
        """Upsert a game session"""
        ...
