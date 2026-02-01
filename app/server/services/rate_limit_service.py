"""
Rate limiting service using Redis.
"""
from typing import Optional
import redis

try:
    from app.server.config import settings
except ModuleNotFoundError:
    from config import settings


class RateLimitService:
    """Service for rate limiting using Redis."""

    def __init__(self, redis_client: Optional[redis.Redis] = None):
        """
        Initialize rate limiting service.

        Args:
            redis_client: Optional Redis client. If not provided, creates a new connection.
        """
        self.redis_client = redis_client
        self._own_connection = redis_client is None

        if self._own_connection and redis_client is None:
            # Create own connection if none provided
            try:
                self.redis_client = redis.from_url(
                    settings.redis_url,
                    encoding="utf-8",
                    decode_responses=True
                )
            except Exception:
                # Gracefully handle Redis connection failures
                self.redis_client = None

    def disconnect(self):
        """Disconnect from Redis server if we own the connection."""
        if self._own_connection and self.redis_client:
            try:
                self.redis_client.close()
            except Exception:
                pass
            self.redis_client = None

    def _get_key(self, identifier: str) -> str:
        """
        Get Redis key for rate limiting identifier.

        Args:
            identifier: Unique identifier (email, IP address, etc.)

        Returns:
            Redis key string
        """
        return f"rate_limit:login:{identifier}"

    def check_rate_limit(self, identifier: str) -> tuple[bool, int]:
        """
        Check if identifier is rate limited.

        Args:
            identifier: Unique identifier to check (email or IP)

        Returns:
            Tuple of (is_locked, attempts_remaining)
            - is_locked: True if rate limit exceeded
            - attempts_remaining: Number of attempts left before lockout
        """
        if not self.redis_client:
            # Redis unavailable, allow request
            return False, settings.rate_limit_max_attempts

        key = self._get_key(identifier)
        attempts = self.redis_client.get(key)  # type: ignore

        if attempts is None:
            # No attempts yet
            return False, settings.rate_limit_max_attempts

        current_attempts = int(attempts)

        if current_attempts >= settings.rate_limit_max_attempts:
            # Rate limit exceeded
            return True, 0

        # Still have attempts remaining
        remaining = settings.rate_limit_max_attempts - current_attempts
        return False, remaining

    def increment_failed_attempts(self, identifier: str) -> int:
        """
        Increment failed login attempts counter.

        Args:
            identifier: Unique identifier (email or IP)

        Returns:
            Current number of failed attempts
        """
        if not self.redis_client:
            # Redis unavailable, return 0
            return 0

        key = self._get_key(identifier)
        current = self.redis_client.get(key)  # type: ignore

        if current is None:
            # First failed attempt
            self.redis_client.setex(  # type: ignore
                key,
                settings.rate_limit_lockout_minutes * 60,  # Convert to seconds
                1
            )
            return 1
        else:
            # Increment existing counter
            new_count = self.redis_client.incr(key)  # type: ignore

            # If this is the max attempt, set expiry for lockout period
            if new_count == settings.rate_limit_max_attempts:
                self.redis_client.expire(  # type: ignore
                    key,
                    settings.rate_limit_lockout_minutes * 60
                )

            return int(new_count)

    def reset_failed_attempts(self, identifier: str) -> None:
        """
        Reset failed login attempts counter.

        Called on successful login.

        Args:
            identifier: Unique identifier (email or IP)
        """
        if not self.redis_client:
            return

        key = self._get_key(identifier)
        self.redis_client.delete(key)  # type: ignore

    def get_lockout_ttl(self, identifier: str) -> Optional[int]:
        """
        Get remaining time (in seconds) for rate limit lockout.

        Args:
            identifier: Unique identifier (email or IP)

        Returns:
            Seconds remaining until lockout expires, or None if not locked
        """
        if not self.redis_client:
            return None

        key = self._get_key(identifier)
        ttl = self.redis_client.ttl(key)  # type: ignore

        if ttl and ttl > 0:
            return int(ttl)
        return None


# Singleton instance
rate_limit_service = RateLimitService()
