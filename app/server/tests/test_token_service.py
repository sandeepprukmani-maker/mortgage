import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from services.token_service import TokenService
from models.refresh_token import RefreshToken


class TestTokenService:
    """Test suite for token service."""

    def setup_method(self):
        """Setup test token service."""
        self.token_service = TokenService()

    def test_create_access_token_includes_correct_claims(self):
        """Test access token creation includes user_id and email."""
        user_id = 1
        email = "test@example.com"

        token = self.token_service.create_access_token(user_id, email)
        claims = self.token_service.verify_access_token(token)

        assert claims["user_id"] == user_id
        assert claims["email"] == email
        assert "exp" in claims

    def test_verify_access_token_succeeds_with_valid_token(self):
        """Test access token verification succeeds with valid token."""
        user_id = 1
        email = "test@example.com"

        token = self.token_service.create_access_token(user_id, email)
        claims = self.token_service.verify_access_token(token)

        assert claims is not None
        assert claims["user_id"] == user_id
        assert claims["email"] == email

    def test_verify_access_token_fails_with_invalid_signature(self):
        """Test access token verification fails with tampered token."""
        user_id = 1
        email = "test@example.com"

        token = self.token_service.create_access_token(user_id, email)
        tampered_token = token[:-10] + "tampered00"

        with pytest.raises(Exception):
            self.token_service.verify_access_token(tampered_token)

    def test_verify_access_token_fails_with_malformed_token(self):
        """Test access token verification fails with malformed token."""
        with pytest.raises(Exception):
            self.token_service.verify_access_token("not.a.valid.token")

    @pytest.mark.asyncio
    async def test_create_refresh_token_stores_in_database(self, db_session):
        """Test refresh token creation stores token in database."""
        user_id = 1

        refresh_token = await self.token_service.create_refresh_token(user_id, db_session)

        assert refresh_token is not None
        assert refresh_token.user_id == user_id
        assert refresh_token.token is not None
        assert refresh_token.is_revoked is False

        result = await db_session.execute(
            select(RefreshToken).where(RefreshToken.token == refresh_token.token)
        )
        db_token = result.scalar_one_or_none()
        assert db_token is not None
        assert db_token.user_id == user_id

    @pytest.mark.asyncio
    async def test_verify_refresh_token_succeeds_with_valid_token(self, db_session):
        """Test refresh token verification succeeds with valid token."""
        user_id = 1

        refresh_token = await self.token_service.create_refresh_token(user_id, db_session)
        verified_token = await self.token_service.verify_refresh_token(refresh_token.token, db_session)

        assert verified_token is not None
        assert verified_token.user_id == user_id
        assert verified_token.is_revoked is False

    @pytest.mark.asyncio
    async def test_verify_refresh_token_fails_with_revoked_token(self, db_session):
        """Test refresh token verification fails with revoked token."""
        user_id = 1

        refresh_token = await self.token_service.create_refresh_token(user_id, db_session)
        await self.token_service.revoke_refresh_token(refresh_token.token, db_session)

        with pytest.raises(ValueError, match="revoked"):
            await self.token_service.verify_refresh_token(refresh_token.token, db_session)

    @pytest.mark.asyncio
    async def test_verify_refresh_token_fails_with_expired_token(self, db_session):
        """Test refresh token verification fails with expired token."""
        user_id = 1

        # Create a refresh token and manually expire it
        refresh_token = await self.token_service.create_refresh_token(user_id, db_session)
        refresh_token.expires_at = datetime.now(timezone.utc) - timedelta(days=1)
        await db_session.commit()

        with pytest.raises(ValueError, match="expired"):
            await self.token_service.verify_refresh_token(refresh_token.token, db_session)

    @pytest.mark.asyncio
    async def test_verify_refresh_token_fails_with_nonexistent_token(self, db_session):
        """Test refresh token verification fails with non-existent token."""
        with pytest.raises(ValueError, match="Invalid"):
            await self.token_service.verify_refresh_token("nonexistent-token", db_session)

    @pytest.mark.asyncio
    async def test_revoke_refresh_token_marks_as_revoked(self, db_session):
        """Test revoking refresh token marks it as revoked."""
        user_id = 1

        refresh_token = await self.token_service.create_refresh_token(user_id, db_session)
        assert refresh_token.is_revoked is False

        await self.token_service.revoke_refresh_token(refresh_token.token, db_session)

        result = await db_session.execute(
            select(RefreshToken).where(RefreshToken.token == refresh_token.token)
        )
        db_token = result.scalar_one_or_none()
        assert db_token.is_revoked is True

    def test_access_token_expiry_time(self):
        """Test access token has correct expiry time."""
        user_id = 1
        email = "test@example.com"

        token = self.token_service.create_access_token(user_id, email)
        claims = self.token_service.verify_access_token(token)

        exp_timestamp = claims["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        now = datetime.now(timezone.utc)

        time_diff = (exp_datetime - now).total_seconds()
        expected_expiry = 15 * 60  # 15 minutes in seconds

        assert abs(time_diff - expected_expiry) < 5  # Allow 5 seconds tolerance

    @pytest.mark.asyncio
    async def test_refresh_token_expiry_time(self, db_session):
        """Test refresh token has correct expiry time."""
        user_id = 1

        refresh_token = await self.token_service.create_refresh_token(user_id, db_session)

        # Ensure expires_at is timezone-aware for comparison
        expires_at = refresh_token.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        time_diff = (expires_at - datetime.now(timezone.utc)).total_seconds()
        expected_expiry = 7 * 24 * 60 * 60  # 7 days in seconds

        assert abs(time_diff - expected_expiry) < 5  # Allow 5 seconds tolerance

    @pytest.mark.asyncio
    async def test_multiple_refresh_tokens_per_user(self, db_session):
        """Test user can have multiple active refresh tokens."""
        user_id = 1

        token1 = await self.token_service.create_refresh_token(user_id, db_session)
        token2 = await self.token_service.create_refresh_token(user_id, db_session)

        assert token1.token != token2.token

        verified_token1 = await self.token_service.verify_refresh_token(token1.token, db_session)
        verified_token2 = await self.token_service.verify_refresh_token(token2.token, db_session)

        assert verified_token1 is not None
        assert verified_token2 is not None
