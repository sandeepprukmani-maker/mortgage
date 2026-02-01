"""
Authentication-related Pydantic schemas.
"""
import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    """Schema for user registration request."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=255)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password meets security requirements."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePass123",
                "first_name": "John",
                "last_name": "Doe"
            }
        }
    }


class LoginRequest(BaseModel):
    """Schema for user login request."""

    email: EmailStr
    password: str = Field(..., min_length=1)

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePass123"
            }
        }
    }


class ForgotPasswordRequest(BaseModel):
    """Schema for forgot password request."""

    email: EmailStr

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "john.doe@example.com"
            }
        }
    }


class ResetPasswordRequest(BaseModel):
    """Schema for password reset request."""

    token: str = Field(..., description="Password reset token from email")
    new_password: str = Field(..., min_length=8, max_length=255)

    @field_validator('new_password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password meets security requirements."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "token": "550e8400-e29b-41d4-a716-446655440000",
                "new_password": "NewSecurePass123"
            }
        }
    }


class GoogleCallbackRequest(BaseModel):
    """Schema for Google OAuth callback."""

    code: str = Field(..., description="Authorization code from Google OAuth")
    state: Optional[str] = Field(None, description="Optional state parameter for CSRF protection")

    model_config = {
        "json_schema_extra": {
            "example": {
                "code": "4/0AX4XfWh...",
                "state": "random_state_string"
            }
        }
    }


class AuthResponse(BaseModel):
    """Schema for authentication success response."""

    message: str
    user: Optional[dict] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Registration successful. Please login to continue.",
                "user": None
            }
        }
    }


class MessageResponse(BaseModel):
    """Schema for simple message responses."""

    message: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Operation completed successfully"
            }
        }
    }
