from fastapi import APIRouter, Depends, HTTPException, status, Header
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.application.ports.auth_provider import IAuthProvider
from app.application.ports.database_repository import IUserRepository
from app.infrastructure.api.dependencies import get_auth_provider, get_user_repo, get_current_user
from app.domain.schemas import PlayerProfile

router = APIRouter()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    identifier: str # email or username
    password: str

class OnboardingRequest(BaseModel):
    username: str
    character_class: str

@router.get("/email")
async def get_email_by_username(
    username: str,
    user_repo: IUserRepository = Depends(get_user_repo)
):
    """Public endpoint to resolve a username to an email for login purpose"""
    user = await user_repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="Username not found")
    return {"email": user.email}

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    auth_provider: IAuthProvider = Depends(get_auth_provider),
    user_repo: IUserRepository = Depends(get_user_repo)
):
    """
    Initial registration: Creates an entry in Firebase Auth and 
    initializes a barebones PlayerProfile in Firestore.
    """
    # Note: signup is usually handled by Firebase SDK in the frontend,
    # but we can provide an endpoint for completeness or server-side creation.
    # For now, we'll assume the frontend creates the Auth user and then calls
    # this endpoint to "initialize" the Firestore profile.
    
    # In a real app, we'd use auth_provider.create_user here.
    # To keep it simple and follow the "Sign-up only with email/pass" rule:
    pass

@router.get("/me", response_model=PlayerProfile)
async def get_me(current_user: PlayerProfile = Depends(get_current_user)):
    """Returns the profile of the currently authenticated player"""
    return current_user

@router.post("/onboarding")
async def complete_onboarding(
    request: OnboardingRequest,
    authorization: str = Header(..., description="Bearer <token>"),
    auth_provider: IAuthProvider = Depends(get_auth_provider),
    user_repo: IUserRepository = Depends(get_user_repo)
):
    """
    Enriches the player's profile with username and class.
    Must verify token first.
    """
    token = authorization.split("Bearer ")[1]
    claims = await auth_provider.verify_token(token)
    uid = claims.get("uid")
    email = claims.get("email")
    
    # Check if username is taken
    existing = await user_repo.get_user_by_username(request.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already claimed")
    
    # Initialize profile
    new_profile = PlayerProfile(
        user_id=uid,
        email=email,
        username=request.username,
        character_path=request.character_class,
        level=1,
        current_hp=100,
        max_hp=100
    )
    
    await user_repo.save_user(new_profile)
    return {"status": "Linked", "profile": new_profile}

