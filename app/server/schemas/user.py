"""
User-related Pydantic schemas.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class TenantInfo(BaseModel):
    """Tenant information for user profile."""

    id: int
    company_name: str
    plan: str = Field(..., description="Subscription plan: free, basic, premium")
    is_active: bool

    model_config = {"from_attributes": True}


class RoleInfo(BaseModel):
    """Role information for user profile."""

    id: int
    name: str = Field(..., description="Role name: loan_officer, admin, super_admin")
    description: Optional[str] = None

    model_config = {"from_attributes": True}


class PermissionInfo(BaseModel):
    """Permission information."""

    id: int
    name: str
    description: Optional[str] = None
    module: str

    model_config = {"from_attributes": True}


class UserBase(BaseModel):
    """Base user schema with common fields."""

    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """Schema for creating a new user with local authentication."""

    password: str = Field(..., min_length=8, max_length=255)

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "SecurePass123"
            }
        }
    }


class OAuthUserCreate(UserBase):
    """Schema for creating a new user via OAuth (no password required)."""

    google_id: str = Field(..., description="Google user ID")
    avatar_url: Optional[str] = Field(None, description="Profile picture URL")
    is_email_verified: bool = Field(default=False)

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "john.doe@gmail.com",
                "first_name": "John",
                "last_name": "Doe",
                "google_id": "123456789",
                "avatar_url": "https://lh3.googleusercontent.com/...",
                "is_email_verified": True
            }
        }
    }


class UserUpdate(BaseModel):
    """Schema for updating user profile."""

    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "John",
                "last_name": "Doe"
            }
        }
    }


class UserResponse(UserBase):
    """Schema for user response (basic info)."""

    id: int
    auth_provider: str = Field(..., description="Authentication provider: local or google")
    is_email_verified: bool
    avatar_url: Optional[str] = None
    created_at: datetime
    last_login_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class UserProfile(UserResponse):
    """Schema for complete user profile with tenant and role info."""

    tenant: TenantInfo
    role: RoleInfo
    permissions: list[PermissionInfo] = Field(default_factory=list)
    available_modules: list[str] = Field(
        default_factory=list,
        description="Modules available based on subscription plan"
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "auth_provider": "local",
                "is_email_verified": False,
                "avatar_url": None,
                "created_at": "2024-01-01T00:00:00Z",
                "last_login_at": "2024-01-02T12:00:00Z",
                "tenant": {
                    "id": 1,
                    "company_name": "Acme Corp",
                    "plan": "premium",
                    "is_active": True
                },
                "role": {
                    "id": 1,
                    "name": "loan_officer",
                    "description": "Loan officer with access to loan management"
                },
                "permissions": [
                    {"id": 1, "name": "view_loans", "description": "View loans", "module": "loans"},
                    {"id": 2, "name": "create_loans", "description": "Create loans", "module": "loans"}
                ],
                "available_modules": ["loans", "borrowers", "documents", "analytics"]
            }
        }
    }
