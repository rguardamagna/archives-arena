import pytest
from httpx import AsyncClient
from app.main import app
import os

# Note: These tests assume the Firebase Auth Emulator is running 
# and FIREBASE_AUTH_EMULATOR_HOST is set.
@pytest.mark.asyncio
async def test_auth_email_lookup_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/auth/email?username=nonexistent_user")
    assert response.status_code == 404
    assert response.json()["detail"] == "Username not found"

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert "ok" in response.json()["status"]

# We avoid testing the full /me or /onboarding without a valid mock token 
# to avoid complex mocking of firebase_admin.auth in this simple verification.
