"""JWT authentication and authorization for Task CRUD API."""

import logging
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.config import settings

logger = logging.getLogger(__name__)

# Security scheme for HTTP Bearer tokens
# auto_error=False so we can consistently return 401 (not 403) on missing tokens.
security = HTTPBearer(auto_error=False)

# JWT algorithm
ALGORITHM = "HS256"


class TokenPayload:
    """JWT token payload."""

    def __init__(self, user_id: str):
        """Initialize token payload.

        Args:
            user_id: The authenticated user's ID (string from Better Auth)
        """
        self.user_id = user_id


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> str:
    """Extract and verify user ID from JWT token.

    Args:
        credentials: HTTP Bearer authentication credentials

    Returns:
        User ID (string) extracted from JWT token

    Raises:
        HTTPException: 401 if token is missing or invalid
    """
    if not credentials or not credentials.credentials:
        logger.warning("Missing JWT token in request")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        # Verify JWT signature using shared secret
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=[ALGORITHM],
        )

        # Extract user_id from 'sub' claim (string ID from Better Auth)
        user_id = payload.get("sub")

        if not user_id:
            logger.warning("JWT token missing 'sub' claim")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return str(user_id)

    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Unexpected error during JWT verification: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )
