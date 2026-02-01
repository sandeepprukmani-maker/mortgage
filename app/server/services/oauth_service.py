"""
OAuth service for Google authentication.
"""
import logging
from typing import Optional
from urllib.parse import urlencode

import httpx

try:
    from app.server.config import settings
except ModuleNotFoundError:
    from config import settings

logger = logging.getLogger(__name__)

# Mapping of Google OAuth error codes to user-friendly messages
GOOGLE_ERROR_MESSAGES = {
    "invalid_client": "Invalid Google OAuth credentials. Please verify GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET are correct.",
    "invalid_grant": "Authorization code expired or already used. Please try signing in again.",
    "redirect_uri_mismatch": "OAuth redirect URI mismatch. Please verify GOOGLE_REDIRECT_URI matches Google Cloud Console configuration.",
    "unauthorized_client": "Application not authorized for this OAuth grant type. Please check Google Cloud Console settings.",
    "access_denied": "Access was denied. Please try signing in again and grant the required permissions.",
    "invalid_request": "Invalid OAuth request. Please try signing in again.",
}


class OAuthService:
    """Service for Google OAuth 2.0 authentication."""

    def __init__(self):
        """Initialize OAuth configuration."""
        self.client_id = settings.google_client_id
        self.client_secret = settings.google_client_secret
        self.redirect_uri = settings.google_redirect_uri
        self.token_url = "https://oauth2.googleapis.com/token"
        self.userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        self.authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"

    def is_configured(self) -> bool:
        """
        Check if Google OAuth is properly configured.

        Returns:
            True if both client_id and client_secret are set, False otherwise
        """
        return bool(self.client_id and self.client_secret)

    def validate_credentials(self) -> None:
        """
        Validate that OAuth credentials are configured.

        Raises:
            ValueError: If credentials are not configured
        """
        if not self.client_id:
            raise ValueError(
                "Google OAuth is not configured. "
                "Please set GOOGLE_CLIENT_ID in your environment."
            )
        if not self.client_secret:
            raise ValueError(
                "Google OAuth is not configured. "
                "Please set GOOGLE_CLIENT_SECRET in your environment."
            )

    def get_google_authorization_url(self, state: Optional[str] = None) -> str:
        """
        Generate Google OAuth authorization URL.

        Args:
            state: Optional state parameter for CSRF protection

        Returns:
            Authorization URL for redirecting user to Google

        Raises:
            ValueError: If OAuth credentials are not configured
        """
        # Validate credentials before generating URL
        self.validate_credentials()

        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent",
        }

        if state:
            params["state"] = state

        return f"{self.authorization_base_url}?{urlencode(params)}"

    def _parse_google_error(self, response: httpx.Response) -> str:
        """
        Parse error response from Google OAuth.

        Args:
            response: HTTP response from Google

        Returns:
            User-friendly error message
        """
        try:
            error_data = response.json()
            error_code = error_data.get("error", "")
            error_description = error_data.get("error_description", "")

            # Log the full error for debugging
            logger.error(
                f"Google OAuth error: {error_code} - {error_description}"
            )

            # Return user-friendly message if we have a mapping
            if error_code in GOOGLE_ERROR_MESSAGES:
                return GOOGLE_ERROR_MESSAGES[error_code]

            # Fall back to error description if available
            if error_description:
                return f"Google OAuth error: {error_description}"

            return f"Google OAuth error: {error_code or 'Unknown error'}"
        except Exception:
            # If we can't parse the error, return generic message
            return f"Google OAuth failed with status {response.status_code}. Please try again."

    async def exchange_code_for_token(self, code: str) -> dict:
        """
        Exchange authorization code for access token.

        Args:
            code: Authorization code from Google OAuth callback

        Returns:
            Token response dict containing access_token, token_type, etc.

        Raises:
            ValueError: If token exchange fails or credentials not configured
        """
        # Validate credentials first
        self.validate_credentials()

        data = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.token_url, data=data)

                if response.status_code != 200:
                    error_message = self._parse_google_error(response)
                    raise ValueError(error_message)

                return response.json()
        except httpx.HTTPStatusError as e:
            error_message = self._parse_google_error(e.response)
            raise ValueError(error_message) from e
        except httpx.RequestError as e:
            logger.error(f"Network error during OAuth token exchange: {e}")
            raise ValueError(
                "Unable to connect to Google OAuth service. Please check your network connection."
            ) from e

    async def get_google_user_info(self, access_token: str) -> dict:
        """
        Get user information from Google using access token.

        Args:
            access_token: Google OAuth access token

        Returns:
            User info dict containing id, email, name, picture, etc.

        Raises:
            httpx.HTTPError: If user info request fails
        """
        headers = {"Authorization": f"Bearer {access_token}"}

        async with httpx.AsyncClient() as client:
            response = await client.get(self.userinfo_url, headers=headers)
            response.raise_for_status()
            return response.json()

    async def revoke_google_token(self, token: str) -> bool:
        """
        Revoke a Google OAuth token.

        Args:
            token: Access token or refresh token to revoke

        Returns:
            True if revocation successful, False otherwise
        """
        revoke_url = "https://oauth2.googleapis.com/revoke"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    revoke_url,
                    data={"token": token},
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                return response.status_code == 200
        except httpx.HTTPError:
            return False

    def parse_google_user_data(self, user_info: dict) -> dict:
        """
        Parse Google user info into standardized format.

        Args:
            user_info: Raw user info from Google

        Returns:
            Standardized user data dict
        """
        return {
            "google_id": user_info.get("id"),
            "email": user_info.get("email"),
            "first_name": user_info.get("given_name", ""),
            "last_name": user_info.get("family_name", ""),
            "avatar_url": user_info.get("picture"),
            "is_email_verified": user_info.get("verified_email", False),
        }


# Singleton instance
oauth_service = OAuthService()
