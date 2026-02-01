"""
Authentication service with business logic.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

try:
    from app.server.config import settings
    from app.server.models.user import User
    from app.server.models.tenant import Tenant
    from app.server.models.role import Role
    from app.server.models.refresh_token import RefreshToken
    from app.server.models.password_reset import PasswordResetToken
    from app.server.schemas.auth import RegisterRequest
    from app.server.services.password_service import password_service
    from app.server.services.token_service import token_service
    from app.server.services.rate_limit_service import rate_limit_service
    from app.server.services.oauth_service import oauth_service
    from app.server.services.user_service import user_service
except ModuleNotFoundError:
    from config import settings
    from models.user import User
    from models.tenant import Tenant
    from models.role import Role
    from models.refresh_token import RefreshToken
    from models.password_reset import PasswordResetToken
    from schemas.auth import RegisterRequest
    from services.password_service import password_service
    from services.token_service import token_service
    from services.rate_limit_service import rate_limit_service
    from services.oauth_service import oauth_service
    from services.user_service import user_service


class AuthService:
    """Service for authentication business logic."""

    async def register_user(
        self,
        data: RegisterRequest,
        db: AsyncSession
    ) -> User:
        """
        Register a new user with local authentication.

        Args:
            data: Registration request data
            db: Database session

        Returns:
            Created User instance

        Raises:
            ValueError: If validation fails or email exists
        """
        # Get or create default tenant
        result = await db.execute(
            select(Tenant).where(Tenant.company_name == "Default Organization")
        )
        tenant = result.scalar_one_or_none()

        if not tenant:
            tenant = Tenant(
                company_name="Default Organization",
                plan="free",
                is_active=True
            )
            db.add(tenant)
            await db.flush()

        # Get loan_officer role
        result = await db.execute(
            select(Role).where(Role.name == "loan_officer")
        )
        role = result.scalar_one_or_none()

        if not role:
            # Create default role if it doesn't exist
            role = Role(name="loan_officer", description="Loan Officer")
            db.add(role)
            await db.flush()

        # Create user
        from schemas.user import UserCreate
        user_data = UserCreate(
            email=data.email,
            password=data.password,
            first_name=data.first_name,
            last_name=data.last_name
        )

        user = await user_service.create_user(
            data=user_data,
            tenant_id=tenant.id,
            role_id=role.id,
            db=db,
            auth_provider="local",
            is_email_verified=False
        )

        return user

    async def login_user(
        self,
        email: str,
        password: str,
        db: AsyncSession
    ) -> tuple[str, RefreshToken, User]:
        """
        Authenticate user with email and password.

        Args:
            email: User email
            password: User password
            db: Database session

        Returns:
            Tuple of (access_token, refresh_token, user)

        Raises:
            ValueError: If authentication fails or account locked
        """
        # Check rate limiting
        is_locked, attempts_remaining = rate_limit_service.check_rate_limit(email)
        if is_locked:
            ttl = rate_limit_service.get_lockout_ttl(email)
            raise ValueError(
                f"Too many failed login attempts. "
                f"Account locked for {ttl // 60} more minutes."
            )

        # Look up user
        user = await user_service.get_user_by_email(email, db)
        if not user:
            # Increment rate limit for non-existent users too (prevent enumeration)
            rate_limit_service.increment_failed_attempts(email)
            raise ValueError("Incorrect email or password")

        # Check auth provider
        if user.auth_provider != "local":
            rate_limit_service.increment_failed_attempts(email)
            raise ValueError(
                f"This account uses {user.auth_provider} authentication. "
                "Please sign in with Google."
            )

        # Verify password
        if not user.password_hash or not password_service.verify_password(
            password, user.password_hash
        ):
            rate_limit_service.increment_failed_attempts(email)
            raise ValueError("Incorrect email or password")

        # Successful login - reset rate limiting
        rate_limit_service.reset_failed_attempts(email)

        # Update last login
        await user_service.update_last_login(user.id, db)

        # Generate tokens
        access_token = token_service.create_access_token(user.id, user.email)
        refresh_token = await token_service.create_refresh_token(user.id, db)

        return access_token, refresh_token, user

    async def login_with_google(
        self,
        code: str,
        db: AsyncSession
    ) -> tuple[str, RefreshToken, User]:
        """
        Authenticate or register user with Google OAuth.

        Args:
            code: OAuth authorization code from Google
            db: Database session

        Returns:
            Tuple of (access_token, refresh_token, user)

        Raises:
            ValueError: If OAuth fails or account conflict
        """
        # Exchange code for access token
        token_response = await oauth_service.exchange_code_for_token(code)
        access_token_google = token_response.get("access_token")

        if not access_token_google:
            raise ValueError("Failed to obtain access token from Google")

        # Get user info from Google
        user_info = await oauth_service.get_google_user_info(access_token_google)
        google_data = oauth_service.parse_google_user_data(user_info)

        # Check if user exists by email
        user = await user_service.get_user_by_email(google_data["email"], db)

        if user:
            # User exists - check auth provider
            if user.auth_provider == "local":
                raise ValueError(
                    "An account with this email already exists. "
                    "Please login with your password."
                )
            elif user.auth_provider == "google" and user.google_id != google_data["google_id"]:
                raise ValueError("Account mismatch. Please contact support.")

            # Existing Google user - just login
            await user_service.update_last_login(user.id, db)
        else:
            # New user - auto-register
            # Get or create default tenant
            result = await db.execute(
                select(Tenant).where(Tenant.company_name == "Default Organization")
            )
            tenant = result.scalar_one_or_none()

            if not tenant:
                tenant = Tenant(
                    company_name="Default Organization",
                    plan="free",
                    is_active=True
                )
                db.add(tenant)
                await db.flush()

            # Get loan_officer role
            result = await db.execute(
                select(Role).where(Role.name == "loan_officer")
            )
            role = result.scalar_one_or_none()

            if not role:
                role = Role(name="loan_officer", description="Loan Officer")
                db.add(role)
                await db.flush()

            # Create user
            from schemas.user import OAuthUserCreate
            user_data = OAuthUserCreate(
                email=google_data["email"],
                first_name=google_data["first_name"] or "User",
                last_name=google_data["last_name"] or "",
                google_id=google_data["google_id"],
                avatar_url=google_data["avatar_url"],
                is_email_verified=google_data["is_email_verified"],
            )

            user = await user_service.create_oauth_user(
                data=user_data,
                tenant_id=tenant.id,
                role_id=role.id,
                db=db,
            )

        # Generate tokens
        access_token = token_service.create_access_token(user.id, user.email)
        refresh_token = await token_service.create_refresh_token(user.id, db)

        return access_token, refresh_token, user

    async def logout_user(
        self,
        refresh_token: str,
        db: AsyncSession
    ) -> None:
        """
        Logout user by revoking refresh token.

        Args:
            refresh_token: Refresh token to revoke
            db: Database session

        Raises:
            ValueError: If token not found
        """
        await token_service.revoke_refresh_token(refresh_token, db)

    async def refresh_access_token(
        self,
        refresh_token: str,
        db: AsyncSession
    ) -> tuple[str, RefreshToken]:
        """
        Refresh access token using refresh token.

        Implements refresh token rotation for security.

        Args:
            refresh_token: Current refresh token
            db: Database session

        Returns:
            Tuple of (new_access_token, new_refresh_token)

        Raises:
            ValueError: If refresh token invalid or expired
        """
        # Verify refresh token
        old_token = await token_service.verify_refresh_token(refresh_token, db)

        # Get user
        user = await user_service.get_user_by_id(old_token.user_id, db)
        if not user:
            raise ValueError("User not found")

        # Rotate refresh token
        new_refresh_token = await token_service.rotate_refresh_token(refresh_token, db)

        # Generate new access token
        new_access_token = token_service.create_access_token(user.id, user.email)

        return new_access_token, new_refresh_token

    async def request_password_reset(
        self,
        email: str,
        db: AsyncSession
    ) -> Optional[str]:
        """
        Request password reset for user.

        Always returns None to prevent email enumeration.
        Logs reset link to console for MVP (no email service).

        Args:
            email: User email
            db: Database session

        Returns:
            None (always, for security)
        """
        # Look up user
        user = await user_service.get_user_by_email(email, db)

        if user and user.auth_provider == "local":
            # Generate reset token
            reset_token = PasswordResetToken(
                token=str(uuid4()),
                user_id=user.id,
                expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
                is_used=False
            )
            db.add(reset_token)
            await db.commit()

            # Log reset link (MVP - no email service)
            reset_url = f"{settings.frontend_url}/reset-password/{reset_token.token}"
            print(f"\n{'='*80}")
            print("PASSWORD RESET REQUEST")
            print(f"{'='*80}")
            print(f"User: {user.email}")
            print(f"Reset URL: {reset_url}")
            print("Token expires in 1 hour")
            print(f"{'='*80}\n")

        # Always return None (prevent email enumeration)
        return None

    async def reset_password(
        self,
        token: str,
        new_password: str,
        db: AsyncSession
    ) -> None:
        """
        Reset user password with reset token.

        Args:
            token: Password reset token
            new_password: New password
            db: Database session

        Raises:
            ValueError: If token invalid, expired, or used
        """
        # Look up reset token
        result = await db.execute(
            select(PasswordResetToken).where(PasswordResetToken.token == token)
        )
        reset_token = result.scalar_one_or_none()

        if not reset_token:
            raise ValueError("Invalid or expired reset token")

        if not reset_token.is_valid():
            raise ValueError("Reset token has expired or already been used")

        # Get user
        user = await user_service.get_user_by_id(reset_token.user_id, db)
        if not user:
            raise ValueError("User not found")

        if user.auth_provider != "local":
            raise ValueError("Cannot reset password for OAuth accounts")

        # Validate new password (raises ValueError if invalid)
        password_service.validate_password_strength(new_password)

        # Update password
        user.password_hash = password_service.hash_password(new_password)

        # Mark token as used
        reset_token.is_used = True

        await db.commit()


# Singleton instance
auth_service = AuthService()
