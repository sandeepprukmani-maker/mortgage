"""
Pydantic schemas for request/response validation.
"""
from schemas.auth import (
    RegisterRequest,
    LoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    GoogleCallbackRequest,
    AuthResponse,
)
from schemas.token import (
    TokenResponse,
    TokenRefreshRequest,
)
from schemas.user import (
    UserBase,
    UserCreate,
    OAuthUserCreate,
    UserUpdate,
    UserResponse,
    UserProfile,
    TenantInfo,
    RoleInfo,
)

__all__ = [
    # Auth schemas
    "RegisterRequest",
    "LoginRequest",
    "ForgotPasswordRequest",
    "ResetPasswordRequest",
    "GoogleCallbackRequest",
    "AuthResponse",
    # Token schemas
    "TokenResponse",
    "TokenRefreshRequest",
    # User schemas
    "UserBase",
    "UserCreate",
    "OAuthUserCreate",
    "UserUpdate",
    "UserResponse",
    "UserProfile",
    "TenantInfo",
    "RoleInfo",
]
