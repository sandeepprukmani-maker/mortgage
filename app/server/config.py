"""
Configuration management for Valargen server using Pydantic settings.
"""
from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application Environment
    environment: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Application environment (development uses proxy for UWM)"
    )

    # Database Configuration
    database_url: str = Field(
        default="postgresql://valargen:valargen@localhost:6432/valargen",
        description="PostgreSQL database connection URL"
    )

    # Redis Configuration
    redis_url: str = Field(
        default="redis://localhost:6379",
        description="Redis connection URL for rate limiting and caching"
    )

    # JWT Configuration
    jwt_secret_key: str = Field(
        default="development-secret-key-change-in-production-use-secrets-gen",
        description="Secret key for JWT token signing (CHANGE IN PRODUCTION!)"
    )
    jwt_algorithm: str = Field(
        default="HS256",
        description="JWT signing algorithm"
    )
    access_token_expire_minutes: int = Field(
        default=15,
        description="Access token expiry time in minutes"
    )
    refresh_token_expire_days: int = Field(
        default=7,
        description="Refresh token expiry time in days"
    )

    # Google OAuth Configuration
    google_client_id: str = Field(
        default="",
        description="Google OAuth 2.0 Client ID (from Google Cloud Console)"
    )
    google_client_secret: str = Field(
        default="",
        description="Google OAuth 2.0 Client Secret (from Google Cloud Console)"
    )
    google_redirect_uri: str = Field(
        default="http://localhost:8000/api/auth/google/callback",
        description="Google OAuth callback redirect URI"
    )

    # Frontend Configuration
    frontend_url: str = Field(
        default="http://localhost:5173",
        description="Frontend application URL for CORS and redirects"
    )

    # Password Validation Rules
    password_min_length: int = Field(
        default=8,
        description="Minimum password length"
    )
    password_require_uppercase: bool = Field(
        default=True,
        description="Require at least one uppercase letter in password"
    )
    password_require_number: bool = Field(
        default=True,
        description="Require at least one number in password"
    )

    # Rate Limiting Configuration
    rate_limit_max_attempts: int = Field(
        default=5,
        description="Maximum failed login attempts before lockout"
    )
    rate_limit_lockout_minutes: int = Field(
        default=15,
        description="Account lockout duration in minutes after max attempts"
    )

    # Security Configuration
    cookie_secure: bool = Field(
        default=False,
        description="Use secure flag for cookies (set to True in production with HTTPS)"
    )
    cookie_samesite: Literal["lax", "strict", "none"] = Field(
        default="lax",
        description="SameSite cookie attribute for CSRF protection"
    )

    # Application Configuration
    debug: bool = Field(
        default=True,
        description="Enable debug mode"
    )
    log_level: str = Field(
        default="info",
        description="Logging level"
    )

    # Azure Key Vault Configuration (optional)
    key_vault_name: str = Field(
        default="",
        description="Azure Key Vault name for production secrets"
    )

    # UWM API Configuration
    uwm_sso_url: str = Field(
        default="https://sso.uwm.com/adfs/oauth2/token",
        description="UWM SSO OAuth endpoint for token acquisition"
    )
    uwm_api_url: str = Field(
        default="https://api.uwm.com/instantpricequote/v1/pricequote",
        description="UWM Instant Price Quote API endpoint URL"
    )
    uwm_username: str = Field(
        default="",
        description="UWM API username for OAuth authentication"
    )
    uwm_password: str = Field(
        default="",
        description="UWM API password for OAuth authentication"
    )
    uwm_client_id: str = Field(
        default="",
        description="UWM OAuth client ID"
    )
    uwm_client_secret: str = Field(
        default="",
        description="UWM OAuth client secret"
    )
    uwm_environment: Literal["dev", "staging", "production"] = Field(
        default="dev",
        description="UWM API environment (determines scope URL if uwm_scope not set)"
    )
    uwm_scope: str = Field(
        default="",
        description="UWM OAuth scope URL (overrides environment-based scope if set)"
    )
    uwm_api_timeout: int = Field(
        default=30,
        description="UWM API request timeout in seconds"
    )
    uwm_use_real_api: bool = Field(
        default=False,
        description="Use real UWM API (False = mock responses for development)"
    )
    uwm_proxy_url: str = Field(
        default="",
        description="SOCKS5 proxy URL for UWM API requests (e.g., socks5://localhost:1080)"
    )

    @field_validator("jwt_secret_key")
    @classmethod
    def validate_jwt_secret(cls, v: str) -> str:
        """Warn if using default JWT secret in production."""
        if "development-secret-key" in v.lower():
            import warnings
            warnings.warn(
                "Using default JWT secret key! Generate a secure key for production!",
                UserWarning
            )
        return v

    @property
    def async_database_url(self) -> str:
        """Get async database URL for SQLAlchemy."""
        return self.database_url.replace("postgresql://", "postgresql+asyncpg://")


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Export settings instance
settings = get_settings()
