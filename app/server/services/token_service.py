"""
JWT token generation and validation service.
"""
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

try:
    from app.server.config import settings
    from app.server.models.refresh_token import RefreshToken
except ModuleNotFoundError:
    from config import settings
    from models.refresh_token import RefreshToken


class TokenService:
    """Service for JWT token generation, validation, and management."""

    def create_access_token(self, user_id: int, email: str) -> str:
        """
        Create a JWT access token.

        Args:
            user_id: User ID to encode in token
            email: User email to encode in token

        Returns:
            JWT access token string
        """
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
        expire = datetime.now(timezone.utc) + expires_delta

        to_encode = {
            "user_id": user_id,
            "email": email,
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "type": "access"
        }

        encoded_jwt = jwt.encode(
            to_encode,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm
        )
        return encoded_jwt

    async def create_refresh_token(
        self,
        user_id: int,
        db: AsyncSession
    ) -> RefreshToken:
        """
        Create a refresh token and store in database.

        Args:
            user_id: User ID to associate with token
            db: Database session

        Returns:
            RefreshToken model instance
        """
        expires_delta = timedelta(days=settings.refresh_token_expire_days)
        expires_at = datetime.now(timezone.utc) + expires_delta

        refresh_token = RefreshToken(
            token=str(uuid4()),
            user_id=user_id,
            expires_at=expires_at,
            is_revoked=False
        )

        db.add(refresh_token)
        await db.commit()
        await db.refresh(refresh_token)

        return refresh_token

    def verify_access_token(self, token: str) -> dict:
        """
        Verify and decode a JWT access token.

        Args:
            token: JWT access token to verify

        Returns:
            Decoded token payload

        Raises:
            JWTError: If token is invalid, expired, or malformed
            ValueError: If token type is not 'access'
        """
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm]
            )

            # Verify token type
            if payload.get("type") != "access":
                raise ValueError("Invalid token type")

            return payload

        except JWTError as e:
            raise JWTError(f"Invalid access token: {str(e)}")

    async def verify_refresh_token(
        self,
        token: str,
        db: AsyncSession
    ) -> RefreshToken:
        """
        Verify a refresh token from database.

        Args:
            token: Refresh token UUID string
            db: Database session

        Returns:
            RefreshToken model instance if valid

        Raises:
            ValueError: If token is invalid, expired, or revoked
        """
        # Look up token in database
        result = await db.execute(
            select(RefreshToken).where(RefreshToken.token == token)
        )
        refresh_token = result.scalar_one_or_none()

        if not refresh_token:
            raise ValueError("Invalid refresh token")

        # Check if token is revoked
        if refresh_token.is_revoked:
            raise ValueError("Refresh token has been revoked")

        # Check if token is expired
        if refresh_token.is_expired():
            raise ValueError("Refresh token has expired")

        return refresh_token

    async def revoke_refresh_token(
        self,
        token: str,
        db: AsyncSession
    ) -> None:
        """
        Revoke a refresh token.

        Args:
            token: Refresh token UUID string to revoke
            db: Database session

        Raises:
            ValueError: If token doesn't exist
        """
        result = await db.execute(
            select(RefreshToken).where(RefreshToken.token == token)
        )
        refresh_token = result.scalar_one_or_none()

        if not refresh_token:
            raise ValueError("Refresh token not found")

        refresh_token.is_revoked = True
        await db.commit()

    async def rotate_refresh_token(
        self,
        old_token: str,
        db: AsyncSession
    ) -> RefreshToken:
        """
        Rotate a refresh token (revoke old, create new).

        This implements refresh token rotation for enhanced security.

        Args:
            old_token: Old refresh token to revoke
            db: Database session

        Returns:
            New RefreshToken instance

        Raises:
            ValueError: If old token is invalid
        """
        # Verify and get old token
        old_refresh_token = await self.verify_refresh_token(old_token, db)

        # Revoke old token
        old_refresh_token.is_revoked = True

        # Create new token for same user
        new_refresh_token = await self.create_refresh_token(
            old_refresh_token.user_id,
            db
        )

        await db.commit()

        return new_refresh_token

    async def cleanup_expired_tokens(self, db: AsyncSession) -> int:
        """
        Clean up expired refresh tokens from database.

        This should be run periodically as a maintenance task.

        Args:
            db: Database session

        Returns:
            Number of tokens deleted
        """
        from sqlalchemy import delete

        result = await db.execute(
            delete(RefreshToken).where(
                RefreshToken.expires_at < datetime.now(timezone.utc)
            )
        )
        await db.commit()

        return result.rowcount  # type: ignore


# Singleton instance
token_service = TokenService()
