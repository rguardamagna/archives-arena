from typing import Optional
from google.cloud import firestore
from app.application.ports.database_repository import IUserRepository, IGameSessionRepository
from app.domain.schemas import PlayerProfile, GameSession

class FirestoreUserRepository(IUserRepository, IGameSessionRepository):
    """
    Adapter for Google Cloud Firestore.
    Implements IUserRepository and IGameSessionRepository ports.
    """
    
    def __init__(self, project_id: Optional[str] = None, client: Optional[firestore.AsyncClient] = None):
        self.client = client or firestore.AsyncClient(project=project_id)
        self.user_collection = "players"
        self.session_collection = "sessions"

    async def get_user(self, user_id: str) -> Optional[PlayerProfile]:
        doc_ref = self.client.collection(self.user_collection).document(user_id)
        doc = await doc_ref.get()
        if not doc.exists: return None
        return PlayerProfile(**doc.to_dict())

    async def get_user_by_username(self, username: str) -> Optional[PlayerProfile]:
        """Fetch a user by their unique username alias using a query"""
        query = self.client.collection(self.user_collection).where(filter=firestore.FieldFilter("username", "==", username)).limit(1)
        docs = await query.get()
        if not docs: return None
        return PlayerProfile(**docs[0].to_dict())

    async def save_user(self, user: PlayerProfile) -> None:
        """Upsert a user document into the NoSQL store"""
        doc_ref = self.client.collection(self.user_collection).document(user.user_id)
        await doc_ref.set(user.model_dump(), merge=True)

    async def get_session(self, session_id: str) -> Optional[GameSession]:
        """Fetches a game session document"""
        doc_ref = self.client.collection(self.session_collection).document(session_id)
        doc = await doc_ref.get()
        if not doc.exists: return None
        return GameSession(**doc.to_dict())

    async def save_session(self, session: GameSession) -> None:
        """Upserts a game session document"""
        doc_ref = self.client.collection(self.session_collection).document(session.session_id)
        await doc_ref.set(session.model_dump(), merge=True)
