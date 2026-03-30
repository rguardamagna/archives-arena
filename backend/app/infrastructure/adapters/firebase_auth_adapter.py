import os
import firebase_admin
from firebase_admin import auth, credentials
from typing import Dict, Any, Optional
from app.application.ports.auth_provider import IAuthProvider

class FirebaseAuthAdapter(IAuthProvider):
    """
    Adapter for Firebase Authentication.
    Uses firebase-admin SDK and supports both Cloud and Local Emulator.
    """
    
    def __init__(self):
        # Initialize Firebase Admin if not already initialized
        try:
            firebase_admin.get_app()
        except ValueError:
            # We assume credentials/project are set via env vars or service account file
            project_id = os.getenv("PROJECT_ID")
            if os.getenv("FIREBASE_AUTH_EMULATOR_HOST"):
                # In emulator mode, we don't need real credentials
                firebase_admin.initialize_app(options={'projectId': project_id})
            else:
                cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
                if cred_path and os.path.exists(cred_path):
                    cred = credentials.Certificate(cred_path)
                    firebase_admin.initialize_app(cred)
                else:
                    firebase_admin.initialize_app()

    async def verify_token(self, token: str) -> Dict[str, Any]:
        """Verifies an ID Token and returns user info"""
        # Note: verify_id_token is blocking, in a high-traffic app we might want to run it in a threadpool
        decoded_token = auth.verify_id_token(token)
        return decoded_token

    async def get_user_email(self, uid: str) -> str:
        """Fetch email for a given UID"""
        user = auth.get_user(uid)
        return user.email
