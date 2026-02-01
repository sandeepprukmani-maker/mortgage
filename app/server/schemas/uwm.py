"""
UWM-related Pydantic schemas.
"""
from pydantic import BaseModel, Field


class UWMTestConnectionResponse(BaseModel):
    """Schema for UWM connection test response."""

    success: bool = Field(..., description="Whether connection succeeded")
    outgoing_ip: str | None = Field(None, description="The detected outgoing IP address")
    sso_url: str = Field(..., description="The UWM SSO URL being used")
    client_id: str = Field(..., description="The client ID being used (for display)")
    scope: str = Field(..., description="The OAuth scope being used")
    grant_type: str = Field(..., description="The grant type (password or client_credentials)")
    error: str | None = Field(None, description="Error message if connection failed")
    logs: list[str] = Field(default_factory=list, description="List of log messages from the connection attempt")

    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "outgoing_ip": "x.x.x.x",
                "sso_url": "https://sso.uwm.com/adfs/oauth2/token",
                "client_id": "your-client-id",
                "scope": "https://api.uwm.com/loanorigination-int",
                "grant_type": "client_credentials",
                "error": None,
                "logs": [
                    "Outgoing IP address: x.*.*.*",
                    "Sending OAuth request to: https://sso.uwm.com/adfs/oauth2/token",
                    "Successfully acquired UWM access token"
                ]
            }
        }
    }
