from typing import Protocol, Optional, Dict, Any

class IAuthProvider(Protocol):
    """
    Port for identity and authentication providers.
    Typically used to verify ID Tokens from Firebase, Auth0, etc.
    """
    
    async def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verifies a JWT/ID Token and returns the decoded claims.
        Should raise an exception if the token is invalid or expired.
        """
        ...

    async def get_user_email(self, uid: str) -> str:
        """
        Retrieves the email associated with a UID from the Auth provider.
        """
        ...
