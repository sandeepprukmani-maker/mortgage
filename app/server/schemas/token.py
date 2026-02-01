"""
Token-related Pydantic schemas for JWT authentication.
"""
from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    """Response schema for token endpoints."""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type (always 'bearer')")
    expires_in: int = Field(..., description="Token expiry time in seconds")

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 900
            }
        }
    }


class TokenRefreshRequest(BaseModel):
    """Request schema for token refresh endpoint."""

    # Note: In practice, refresh token comes from HTTPOnly cookie,
    # but we include this schema for API documentation completeness
    pass

    model_config = {
        "json_schema_extra": {
            "example": {},
            "description": "Refresh token is automatically read from HTTPOnly cookie"
        }
    }
