"""
UWM OAuth authentication service for token management.

Handles OAuth 2.0 token acquisition, caching, and refresh for UWM API integration.
"""
import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Optional

import httpx
import redis

try:
    from app.server.config import settings
except ModuleNotFoundError:
    from config import settings

logger = logging.getLogger(__name__)

# Token expiry buffer (refresh 5 minutes before expiry)
TOKEN_EXPIRY_BUFFER_SECONDS = 300

# Redis key prefix for UWM tokens
REDIS_KEY_PREFIX = "uwm:"

# Environment to scope URL mapping
ENVIRONMENT_SCOPES = {
    "dev": "https://api.uwm.com/loanorigination-int",
    "staging": "https://api.uwm.com/loanorigination-stg",
    "production": "https://api.uwm.com/loanorigination",
}

class ListHandler(logging.Handler):
    """Custom log handler that captures log messages to a list."""

    def __init__(self):
        super().__init__()
        self.logs: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.logs.append(self.format(record))


# UWM SSO error messages
UWM_ERROR_MESSAGES = {
    "MSIS7065": "Invalid UWM username or password. Please verify credentials.",
    "MSIS9605": "Invalid UWM client ID or secret. Please verify OAuth credentials.",
    "MSIS9611": "Invalid UWM scope value. Please verify environment configuration.",
    "invalid_grant": "UWM OAuth credentials expired or invalid. Please contact UWM support.",
    "invalid_client": "Invalid UWM OAuth client credentials.",
}


@dataclass
class UWMTokenResponse:
    """Response from UWM OAuth token endpoint."""

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    refresh_token_expires_in: int


class UWMAuthService:
    """Service for UWM OAuth 2.0 authentication and token management."""

    def __init__(self, redis_client: Optional[redis.Redis] = None):
        """
        Initialize UWM auth service.

        Args:
            redis_client: Optional Redis client for token caching.
        """
        self.sso_url = settings.uwm_sso_url
        self.username = settings.uwm_username
        self.password = settings.uwm_password
        self.client_id = settings.uwm_client_id
        self.client_secret = settings.uwm_client_secret
        self.environment = settings.uwm_environment
        self.proxy_url = settings.uwm_proxy_url

        self._redis_client = redis_client
        self._own_connection = redis_client is None
        self._lock = asyncio.Lock()

        if self._own_connection:
            try:
                self._redis_client = redis.from_url(
                    settings.redis_url,
                    encoding="utf-8",
                    decode_responses=True
                )
            except Exception as e:
                logger.warning(f"Failed to connect to Redis for token caching: {e}")
                self._redis_client = None

    def _get_http_client(self, timeout: int = 30) -> httpx.AsyncClient:
        """Get httpx client with optional SOCKS proxy support (development only)."""
        # Only use proxy in development environment
        if self.proxy_url and settings.environment == "development":
            logger.debug(f"Using proxy (development): {self.proxy_url}")
            return httpx.AsyncClient(timeout=timeout, proxy=self.proxy_url)
        return httpx.AsyncClient(timeout=timeout)

    def disconnect(self):
        """Disconnect from Redis if we own the connection."""
        if self._own_connection and self._redis_client:
            try:
                self._redis_client.close()
            except Exception:
                pass
            self._redis_client = None

    def is_configured(self) -> bool:
        """
        Check if UWM OAuth credentials are configured.

        Returns:
            True if required credentials are set.
            Supports both password grant (username/password) and client_credentials grant.
        """
        # Client credentials are always required
        if not (self.client_id and self.client_secret):
            return False
        # Either username/password OR just client credentials (client_credentials grant)
        return True

    def validate_credentials(self) -> None:
        """
        Validate that UWM credentials are configured.

        Raises:
            ValueError: If required credentials are missing.
        """
        missing = []
        if not self.client_id:
            missing.append("UWM_CLIENT_ID")
        if not self.client_secret:
            missing.append("UWM_CLIENT_SECRET")

        if missing:
            raise ValueError(
                f"UWM OAuth credentials not configured. "
                f"Please set: {', '.join(missing)}"
            )

    def _get_grant_type(self) -> str:
        """Determine OAuth grant type based on available credentials."""
        if self.username and self.password:
            return "password"
        return "client_credentials"

    def _get_scope_url(self) -> str:
        """Get OAuth scope URL from direct setting or environment."""
        # Use direct scope if provided
        if settings.uwm_scope:
            return settings.uwm_scope
        # Otherwise derive from environment
        return ENVIRONMENT_SCOPES.get(
            self.environment,
            ENVIRONMENT_SCOPES["dev"]
        )

    def _get_redis_key(self, key_name: str) -> str:
        """Get Redis key with prefix."""
        return f"{REDIS_KEY_PREFIX}{key_name}"

    def _get_cached_access_token(self) -> Optional[str]:
        """Get cached access token from Redis if valid."""
        if not self._redis_client:
            return None

        try:
            token = self._redis_client.get(self._get_redis_key("access_token"))
            expiry = self._redis_client.get(self._get_redis_key("token_expiry"))

            if token and expiry:
                expiry_time = float(expiry)
                # Check if token is still valid (with buffer)
                if time.time() < (expiry_time - TOKEN_EXPIRY_BUFFER_SECONDS):
                    logger.debug("Using cached UWM access token")
                    return token
        except Exception as e:
            logger.warning(f"Failed to get cached token: {e}")

        return None

    def _get_cached_refresh_token(self) -> Optional[str]:
        """Get cached refresh token from Redis if valid."""
        if not self._redis_client:
            return None

        try:
            token = self._redis_client.get(self._get_redis_key("refresh_token"))
            expiry = self._redis_client.get(self._get_redis_key("refresh_expiry"))

            if token and expiry:
                expiry_time = float(expiry)
                if time.time() < expiry_time:
                    return token
        except Exception as e:
            logger.warning(f"Failed to get cached refresh token: {e}")

        return None

    def _cache_tokens(self, token_response: UWMTokenResponse) -> None:
        """Cache tokens in Redis with appropriate TTL."""
        if not self._redis_client:
            return

        try:
            current_time = time.time()

            # Cache access token
            access_expiry = current_time + token_response.expires_in
            self._redis_client.setex(
                self._get_redis_key("access_token"),
                token_response.expires_in,
                token_response.access_token
            )
            self._redis_client.setex(
                self._get_redis_key("token_expiry"),
                token_response.expires_in,
                str(access_expiry)
            )

            # Cache refresh token
            refresh_expiry = current_time + token_response.refresh_token_expires_in
            self._redis_client.setex(
                self._get_redis_key("refresh_token"),
                token_response.refresh_token_expires_in,
                token_response.refresh_token
            )
            self._redis_client.setex(
                self._get_redis_key("refresh_expiry"),
                token_response.refresh_token_expires_in,
                str(refresh_expiry)
            )

            logger.debug("Cached UWM tokens in Redis")
        except Exception as e:
            logger.warning(f"Failed to cache tokens: {e}")

    def clear_cached_tokens(self) -> None:
        """Clear all cached tokens from Redis."""
        if not self._redis_client:
            return

        try:
            keys = [
                self._get_redis_key("access_token"),
                self._get_redis_key("token_expiry"),
                self._get_redis_key("refresh_token"),
                self._get_redis_key("refresh_expiry"),
            ]
            self._redis_client.delete(*keys)
            logger.debug("Cleared cached UWM tokens")
        except Exception as e:
            logger.warning(f"Failed to clear cached tokens: {e}")

    def _parse_uwm_error(self, response: httpx.Response) -> str:
        """Parse error response from UWM SSO."""
        try:
            error_data = response.json()
            error_code = error_data.get("error", "")
            error_description = error_data.get("error_description", "")

            logger.error(f"UWM OAuth error: {error_code} - {error_description}")

            # Check for known error codes in description
            for code, message in UWM_ERROR_MESSAGES.items():
                if code in error_description or code == error_code:
                    return message

            if error_description:
                return f"UWM OAuth error: {error_description}"

            return f"UWM OAuth error: {error_code or 'Unknown error'}"
        except Exception:
            return f"UWM OAuth failed with status {response.status_code}"

    async def _log_outgoing_ip(self, client: httpx.AsyncClient) -> None:
        """Log the outgoing IP address used for API requests (masked)."""
        try:
            ip_response = await client.get("https://api.ipify.org?format=json", timeout=5)
            if ip_response.status_code == 200:
                ip_data = ip_response.json()
                ip = ip_data.get('ip', 'unknown')
                # Mask IP in logs (show first octet only)
                ip_masked = f"{ip.split('.')[0]}.*.*.*" if ip and ip != 'unknown' else "Unknown"
                logger.info(f"Outgoing IP address: {ip_masked}")
        except Exception as e:
            logger.warning(f"Failed to determine outgoing IP: {e}")

    async def _acquire_token(self) -> UWMTokenResponse:
        """
        Acquire new access token using appropriate OAuth grant type.

        Supports both:
        - password grant (when username/password provided)
        - client_credentials grant (when only client_id/secret provided)

        Returns:
            UWMTokenResponse with access and refresh tokens.

        Raises:
            ValueError: If token acquisition fails.
        """
        self.validate_credentials()

        grant_type = self._get_grant_type()
        logger.info(f"Acquiring UWM token using {grant_type} grant")

        data = {
            "grant_type": grant_type,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": self._get_scope_url(),
        }

        # Add username/password for password grant
        if grant_type == "password":
            data["username"] = self.username
            data["password"] = self.password

        try:
            async with self._get_http_client(timeout=30) as client:
                # Log outgoing IP for debugging
                await self._log_outgoing_ip(client)

                logger.info(f"Sending OAuth request to: {self.sso_url}")
                # Log request params (mask all sensitive fields)
                client_id_masked = f"{self.client_id[:20]}***" if self.client_id and len(self.client_id) > 20 else "***"
                scope_masked = f"{data.get('scope', '')[:30]}***" if data.get("scope") and len(data.get("scope", "")) > 30 else "***"
                log_data = {
                    "grant_type": data.get("grant_type"),
                    "client_id": client_id_masked,
                    "client_secret": "***",
                    "scope": scope_masked,
                    "username": data.get("username"),
                    "password": "***" if data.get("password") else None,
                }
                logger.info(f"Request body params: {log_data}")
                response = await client.post(
                    self.sso_url,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )

                if response.status_code != 200:
                    error_message = self._parse_uwm_error(response)
                    raise ValueError(error_message)

                token_data = response.json()
                logger.info("Successfully acquired UWM access token")

                return UWMTokenResponse(
                    access_token=token_data["access_token"],
                    token_type=token_data.get("token_type", "bearer"),
                    expires_in=token_data.get("expires_in", 3600),
                    refresh_token=token_data.get("refresh_token", ""),
                    refresh_token_expires_in=token_data.get("refresh_token_expires_in", 57599),
                )
        except httpx.RequestError as e:
            logger.error(f"Network error during UWM token acquisition: {e}")
            raise ValueError(
                "Unable to connect to UWM OAuth service. "
                "Please check your network connection."
            ) from e

    async def _refresh_access_token(self, refresh_token: str) -> UWMTokenResponse:
        """
        Refresh access token using refresh token.

        Args:
            refresh_token: Valid refresh token.

        Returns:
            UWMTokenResponse with new access and refresh tokens.

        Raises:
            ValueError: If token refresh fails.
        """
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
        }

        try:
            async with self._get_http_client(timeout=30) as client:
                response = await client.post(
                    self.sso_url,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )

                if response.status_code != 200:
                    error_message = self._parse_uwm_error(response)
                    raise ValueError(error_message)

                token_data = response.json()
                logger.info("Successfully refreshed UWM access token")

                return UWMTokenResponse(
                    access_token=token_data["access_token"],
                    token_type=token_data.get("token_type", "bearer"),
                    expires_in=token_data.get("expires_in", 3600),
                    refresh_token=token_data.get("refresh_token", refresh_token),
                    refresh_token_expires_in=token_data.get("refresh_token_expires_in", 57599),
                )
        except httpx.RequestError as e:
            logger.error(f"Network error during UWM token refresh: {e}")
            raise ValueError(
                "Unable to connect to UWM OAuth service for token refresh."
            ) from e

    async def get_access_token(self) -> str:
        """
        Get a valid UWM access token.

        This method implements the following logic:
        1. Check Redis cache for valid access token
        2. If expired, try to refresh using cached refresh token
        3. If no valid refresh token, acquire new tokens using credentials

        Returns:
            Valid access token string.

        Raises:
            ValueError: If unable to obtain access token.
        """
        # First check cache without lock
        cached_token = self._get_cached_access_token()
        if cached_token:
            return cached_token

        # Need to refresh/acquire - use lock to prevent race conditions
        async with self._lock:
            # Double-check cache after acquiring lock
            cached_token = self._get_cached_access_token()
            if cached_token:
                return cached_token

            # Try to refresh using cached refresh token
            refresh_token = self._get_cached_refresh_token()
            if refresh_token:
                try:
                    token_response = await self._refresh_access_token(refresh_token)
                    self._cache_tokens(token_response)
                    return token_response.access_token
                except ValueError as e:
                    logger.warning(f"Token refresh failed, will re-authenticate: {e}")
                    self.clear_cached_tokens()

            # Acquire new tokens using credentials
            token_response = await self._acquire_token()
            self._cache_tokens(token_response)
            return token_response.access_token

    async def get_authorization_header(self) -> dict[str, str]:
        """
        Get authorization header with valid bearer token.

        Returns:
            Dictionary with Authorization header.
        """
        token = await self.get_access_token()
        return {"Authorization": f"Bearer {token}"}

    async def test_connection(self) -> dict:
        """
        Test the UWM OAuth connection and return detailed results.

        Returns:
            Dictionary with connection status, IP, credentials info, and logs.
        """
        # Set up log capture (message only, no prefix)
        handler = ListHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(handler)

        outgoing_ip: str | None = None
        error_message: str | None = None
        success = False

        try:
            # Get IP address
            async with self._get_http_client(timeout=5) as client:
                try:
                    ip_response = await client.get("https://api.ipify.org?format=json")
                    if ip_response.status_code == 200:
                        ip_data = ip_response.json()
                        outgoing_ip = ip_data.get("ip")
                        # Mask IP in logs (show first octet only)
                        ip_masked = f"{outgoing_ip.split('.')[0]}.*.*.*" if outgoing_ip else "Unknown"
                        logger.info(f"Outgoing IP address: {ip_masked}")
                except Exception as e:
                    logger.warning(f"Failed to determine outgoing IP: {e}")

            # Attempt to acquire token
            await self._acquire_token()
            success = True

        except ValueError as e:
            error_message = str(e)
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            logger.error(f"Test connection failed: {e}")
        finally:
            logger.removeHandler(handler)

        return {
            "success": success,
            "outgoing_ip": outgoing_ip,
            "sso_url": self.sso_url,
            "client_id": self.client_id,
            "scope": self._get_scope_url(),
            "grant_type": self._get_grant_type(),
            "error": error_message,
            "logs": handler.logs,
        }


# Singleton instance
uwm_auth_service = UWMAuthService()
