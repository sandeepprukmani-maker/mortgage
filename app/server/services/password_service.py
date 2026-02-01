"""
Password hashing and validation service using Argon2.
"""
import re
from passlib.context import CryptContext

try:
    from app.server.config import settings
except ModuleNotFoundError:
    from config import settings


class PasswordService:
    """Service for password hashing and validation using Argon2."""

    def __init__(self):
        """Initialize password context with Argon2 algorithm."""
        self.pwd_context = CryptContext(
            schemes=["argon2"],
            deprecated="auto",
            argon2__memory_cost=65536,  # 64 MB
            argon2__time_cost=3,  # 3 iterations
            argon2__parallelism=4,  # 4 parallel threads
        )

    def hash_password(self, password: str) -> str:
        """
        Hash a password using Argon2.

        Args:
            password: Plain text password to hash

        Returns:
            Hashed password string

        Raises:
            ValueError: If password is empty
        """
        if not password:
            raise ValueError("Password cannot be empty")
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password.

        Args:
            plain_password: Plain text password to verify
            hashed_password: Hashed password to compare against

        Returns:
            True if password matches, False otherwise
        """
        try:
            return self.pwd_context.verify(plain_password, hashed_password)
        except Exception:
            # Return False for any verification errors (invalid hash, etc.)
            return False

    def validate_password_strength(self, password: str) -> bool:
        """
        Validate password meets security requirements.

        Requirements:
        - Minimum length (from config)
        - At least 1 uppercase letter (if required by config)
        - At least 1 number (if required by config)

        Args:
            password: Password to validate

        Returns:
            True if password is valid

        Raises:
            ValueError: If password doesn't meet requirements
        """
        errors = []

        # Check minimum length
        if len(password) < settings.password_min_length:
            errors.append(
                f"Password must be at least {settings.password_min_length} characters long"
            )

        # Check for uppercase letter
        if settings.password_require_uppercase and not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")

        # Check for number
        if settings.password_require_number and not re.search(r'\d', password):
            errors.append("Password must contain at least one number")

        if errors:
            raise ValueError(". ".join(errors))

        return True

    def needs_rehash(self, hashed_password: str) -> bool:
        """
        Check if a hashed password needs to be rehashed.

        This is useful when password hashing parameters are updated.

        Args:
            hashed_password: Hashed password to check

        Returns:
            True if password needs rehashing, False otherwise
        """
        return self.pwd_context.needs_update(hashed_password)


# Singleton instance
password_service = PasswordService()
