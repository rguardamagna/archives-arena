from fastapi import Depends, Header, HTTPException, status
from app.application.ports.auth_provider import IAuthProvider
from app.application.ports.database_repository import IUserRepository
from app.infrastructure.adapters.firebase_auth_adapter import FirebaseAuthAdapter
from app.infrastructure.adapters.firestore_repository import FirestoreUserRepository
from app.domain.schemas import PlayerProfile
import os

# --- 1. Port injection (Manual DI for now) ---
def get_auth_provider() -> IAuthProvider:
    return FirebaseAuthAdapter()

def get_user_repo() -> IUserRepository:
    # Requires PROJECT_ID to be set in .env
    return FirestoreUserRepository(project_id=os.getenv("PROJECT_ID"))

# --- 2. Security Dependency ---
async def get_current_user(
    authorization: str = Header(..., description="Bearer <token>"),
    auth_provider: IAuthProvider = Depends(get_auth_provider),
    user_repo: IUserRepository = Depends(get_user_repo)
) -> PlayerProfile:
    """
    FastAPI dependency to extract and verify the auth token.
    Returns the PlayerProfile if valid, otherwise raises 401.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme"
        )
    
    token = authorization.split("Bearer ")[1]
    
    try:
        # Step 1: Verify token with Firebase (Emulator or Cloud)
        claims = await auth_provider.verify_token(token)
        uid = claims.get("uid")
        
        # Step 2: Fetch profile from DB
        user = await user_repo.get_user(uid)
        
        if not user:
            # This happens if a user exists in Auth but not in our Firestore DB
            # We will handle automated registration in the auth router, 
            # for now we allow the dependency to fail or return a "partial" user if needed.
            # Rationale: Security First.
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User profile not initialized"
            )
            
        return user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )
