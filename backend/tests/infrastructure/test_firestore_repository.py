import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.infrastructure.adapters.firestore_repository import FirestoreUserRepository
from app.domain.schemas import PlayerProfile, GameSession

@pytest.fixture
def mock_firestore_client():
    client = MagicMock()
    # Mock the chain: client.collection("players").document(user_id).get()
    client.collection = MagicMock()
    return client

@pytest.mark.asyncio
async def test_get_user_success(mock_firestore_client):
    # Setup
    user_id = "test_user_123"
    mock_doc = MagicMock() # Snapshot is not awaited, its .get() is
    mock_doc.to_dict.return_value = {
        "user_id": user_id,
        "email": "test@example.com",
        "character_path": "backend_knight",
        "current_hp": 100,
        "max_hp": 100,
        "level": 2,
        "skills": [],
        "unlocked_nodes": []
    }
    mock_doc.exists = True
    
    # The chain: client.collection("players").document(user_id)
    doc_ref = MagicMock()
    doc_ref.get = AsyncMock(return_value=mock_doc) # .get() IS awaited
    
    mock_firestore_client.collection.return_value.document.return_value = doc_ref
    
    repo = FirestoreUserRepository(client=mock_firestore_client)
    
    # Execute
    result = await repo.get_user(user_id)
    
    # Assert
    assert result is not None
    assert isinstance(result, PlayerProfile)
    assert result.user_id == user_id
    assert result.current_hp == 100
    assert result.level == 2

@pytest.mark.asyncio
async def test_get_user_not_found(mock_firestore_client):
    # Setup
    user_id = "missing_user"
    mock_doc = MagicMock()
    mock_doc.exists = False
    
    doc_ref = MagicMock()
    doc_ref.get = AsyncMock(return_value=mock_doc)
    
    mock_firestore_client.collection.return_value.document.return_value = doc_ref
    
    repo = FirestoreUserRepository(client=mock_firestore_client)
    
    # Execute
    result = await repo.get_user(user_id)
    
    # Assert
    assert result is None

@pytest.mark.asyncio
async def test_save_user_calls_set(mock_firestore_client):
    # Setup
    user = PlayerProfile(user_id="new_user", email="new@example.com", character_path="knight")
    doc_ref = MagicMock()
    doc_ref.set = AsyncMock() # .set() IS awaited
    
    mock_firestore_client.collection.return_value.document.return_value = doc_ref
    
    repo = FirestoreUserRepository(client=mock_firestore_client)
    
    # Execute
    await repo.save_user(user)
    
    # Assert
    doc_ref.set.assert_called_once_with(user.model_dump(), merge=True)

@pytest.mark.asyncio
async def test_get_session_success(mock_firestore_client):
    # Setup
    session_id = "user1_videoA"
    mock_doc = MagicMock()
    mock_doc.to_dict.return_value = {
        "session_id": session_id,
        "user_id": "user1",
        "video_id": "videoA",
        "enemy": {"video_id": "videoA", "max_hp": 100, "current_hp": 100, "topic": "Python"},
        "is_active": True,
        "created_at": "2026-03-20T12:00:00Z"
    }
    mock_doc.exists = True
    
    doc_ref = MagicMock()
    doc_ref.get = AsyncMock(return_value=mock_doc)
    mock_firestore_client.collection.return_value.document.return_value = doc_ref
    
    repo = FirestoreUserRepository(client=mock_firestore_client)
    
    # Execute
    result = await repo.get_session(session_id)
    
    # Assert
    assert result is not None
    assert result.session_id == session_id
    assert result.enemy.topic == "Python"

@pytest.mark.asyncio
async def test_save_session_calls_set(mock_firestore_client):
    # Setup
    enemy = {"video_id": "vid1", "max_hp": 50, "current_hp": 50, "topic": "Test"}
    session = GameSession(session_id="sess1", user_id="u1", video_id="vid1", enemy=enemy)
    
    doc_ref = MagicMock()
    doc_ref.set = AsyncMock()
    mock_firestore_client.collection.return_value.document.return_value = doc_ref
    
    repo = FirestoreUserRepository(client=mock_firestore_client)
    
    # Execute
    await repo.save_session(session)
    
    # Assert
    doc_ref.set.assert_called_once_with(session.model_dump(), merge=True)
