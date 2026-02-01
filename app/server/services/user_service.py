"""
User management service.
"""
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

try:
    from app.server.models.user import User
    from app.server.models.role import Role
    from app.server.schemas.user import UserCreate, UserUpdate, OAuthUserCreate
    from app.server.services.password_service import password_service
except ModuleNotFoundError:
    from models.user import User
    from models.role import Role
    from schemas.user import UserCreate, UserUpdate, OAuthUserCreate
    from services.password_service import password_service


class UserService:
    """Service for user management operations."""

    # Module availability by subscription plan
    PLAN_MODULES = {
        "free": ["dashboard"],
        "basic": ["dashboard", "loans", "borrowers"],
        "premium": ["dashboard", "loans", "borrowers", "documents", "analytics", "automation"],
    }

    async def create_user(
        self,
        data: UserCreate,
        tenant_id: int,
        role_id: int,
        db: AsyncSession,
        auth_provider: str = "local",
        google_id: Optional[str] = None,
        avatar_url: Optional[str] = None,
        is_email_verified: bool = False,
    ) -> User:
        """
        Create a new user.

        Args:
            data: User creation data
            tenant_id: Tenant ID to associate user with
            role_id: Role ID to assign to user
            db: Database session
            auth_provider: Authentication provider (local or google)
            google_id: Google user ID for OAuth users
            avatar_url: Profile picture URL
            is_email_verified: Email verification status

        Returns:
            Created User instance

        Raises:
            ValueError: If email already exists or validation fails
        """
        # Check if email already exists
        existing_user = await self.get_user_by_email(data.email, db)
        if existing_user:
            raise ValueError("Email already registered")

        # Hash password if provided (local auth)
        password_hash = None
        if hasattr(data, 'password') and data.password:
            # Validate password strength (raises ValueError if invalid)
            password_service.validate_password_strength(data.password)
            password_hash = password_service.hash_password(data.password)

        # Create user
        user = User(
            email=data.email,
            password_hash=password_hash,
            first_name=data.first_name,
            last_name=data.last_name,
            auth_provider=auth_provider,
            google_id=google_id,
            is_email_verified=is_email_verified,
            avatar_url=avatar_url,
            tenant_id=tenant_id,
            role_id=role_id,
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user

    async def create_oauth_user(
        self,
        data: OAuthUserCreate,
        tenant_id: int,
        role_id: int,
        db: AsyncSession,
    ) -> User:
        """
        Create a new user via OAuth (no password required).

        Args:
            data: OAuth user creation data
            tenant_id: Tenant ID to associate user with
            role_id: Role ID to assign to user
            db: Database session

        Returns:
            Created User instance

        Raises:
            ValueError: If email already exists
        """
        # Check if email already exists
        existing_user = await self.get_user_by_email(data.email, db)
        if existing_user:
            raise ValueError("Email already registered")

        # Create user (no password for OAuth users)
        user = User(
            email=data.email,
            password_hash=None,
            first_name=data.first_name,
            last_name=data.last_name,
            auth_provider="google",
            google_id=data.google_id,
            is_email_verified=data.is_email_verified,
            avatar_url=data.avatar_url,
            tenant_id=tenant_id,
            role_id=role_id,
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user

    async def get_user_by_email(
        self,
        email: str,
        db: AsyncSession
    ) -> Optional[User]:
        """Get user by email address."""
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_user_by_id(
        self,
        user_id: int,
        db: AsyncSession
    ) -> Optional[User]:
        """Get user by ID."""
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_by_google_id(
        self,
        google_id: str,
        db: AsyncSession
    ) -> Optional[User]:
        """Get user by Google ID."""
        result = await db.execute(
            select(User).where(User.google_id == google_id)
        )
        return result.scalar_one_or_none()

    async def update_last_login(
        self,
        user_id: int,
        db: AsyncSession
    ) -> None:
        """Update user's last login timestamp and reset failed attempts."""
        user = await self.get_user_by_id(user_id, db)
        if user:
            user.last_login_at = datetime.now(timezone.utc)
            user.failed_login_attempts = 0
            user.locked_until = None
            await db.commit()

    async def update_failed_login_attempts(
        self,
        user_id: int,
        increment: bool,
        db: AsyncSession
    ) -> None:
        """Update failed login attempts counter."""
        user = await self.get_user_by_id(user_id, db)
        if user:
            if increment:
                user.failed_login_attempts += 1
            else:
                user.failed_login_attempts = 0
            await db.commit()

    async def get_user_profile(
        self,
        user_id: int,
        db: AsyncSession
    ) -> Optional[dict]:
        """
        Get complete user profile with tenant, role, and permissions.

        Returns:
            User profile dict with all related data
        """
        result = await db.execute(
            select(User)
            .options(
                selectinload(User.tenant),
                selectinload(User.role).selectinload(Role.permissions)
            )
            .where(User.id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            return None

        # Get available modules based on tenant's subscription plan
        available_modules = self.PLAN_MODULES.get(user.tenant.plan, ["dashboard"])

        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "auth_provider": user.auth_provider,
            "is_email_verified": user.is_email_verified,
            "avatar_url": user.avatar_url,
            "created_at": user.created_at,
            "last_login_at": user.last_login_at,
            "tenant": {
                "id": user.tenant.id,
                "company_name": user.tenant.company_name,
                "plan": user.tenant.plan,
                "is_active": user.tenant.is_active,
            },
            "role": {
                "id": user.role.id,
                "name": user.role.name,
                "description": user.role.description,
            },
            "permissions": [
                {
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                    "module": p.module,
                }
                for p in user.role.permissions
            ],
            "available_modules": available_modules,
        }

    async def update_user(
        self,
        user_id: int,
        data: UserUpdate,
        db: AsyncSession
    ) -> Optional[User]:
        """Update user profile."""
        user = await self.get_user_by_id(user_id, db)
        if not user:
            return None

        if data.first_name is not None:
            user.first_name = data.first_name
        if data.last_name is not None:
            user.last_name = data.last_name

        user.updated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(user)

        return user


# Singleton instance
user_service = UserService()
