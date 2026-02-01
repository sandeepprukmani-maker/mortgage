"""
Database models for Valargen application.
"""
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all database models."""
    pass


# Import models to ensure they're registered with SQLAlchemy
from models.tenant import Tenant  # noqa: E402, F401
from models.role import Role  # noqa: E402, F401
from models.permission import Permission, RolePermission  # noqa: E402, F401
from models.user import User  # noqa: E402, F401
from models.refresh_token import RefreshToken  # noqa: E402, F401
from models.password_reset import PasswordResetToken  # noqa: E402, F401
from models.customer import Customer  # noqa: E402, F401
from models.pricing_quote import PricingQuote  # noqa: E402, F401


__all__ = [
    "Base",
    "Tenant",
    "Role",
    "Permission",
    "RolePermission",
    "User",
    "RefreshToken",
    "PasswordResetToken",
    "Customer",
    "PricingQuote",
]
