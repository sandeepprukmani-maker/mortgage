"""Azure Key Vault integration for secrets management.

Uses Managed Identity in Azure, falls back to environment variables locally.
"""

import os
import logging
from functools import lru_cache

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import AzureError

logger = logging.getLogger(__name__)

# Key Vault configuration
KEY_VAULT_NAME = os.getenv("KEY_VAULT_NAME", "valargen-kv")
KEY_VAULT_URL = f"https://{KEY_VAULT_NAME}.vault.azure.net"

# Secret name mappings: env var name -> Key Vault secret name
SECRET_MAPPINGS = {
    "DATABASE_URL": "postgres-password",  # Will construct URL from password
    "REDIS_KEY": "redis-key",
    "STORAGE_KEY": "storage-key",
    "PUBSUB_CONN": "pubsub-conn",
}

_client: SecretClient | None = None
_secrets_cache: dict[str, str] = {}


def _get_client() -> SecretClient | None:
    """Get or create Key Vault client using Managed Identity."""
    global _client
    if _client is not None:
        return _client

    try:
        credential = DefaultAzureCredential()
        _client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)
        logger.info(f"Connected to Key Vault: {KEY_VAULT_NAME}")
        return _client
    except AzureError as e:
        logger.warning(f"Failed to connect to Key Vault: {e}")
        return None


def get_secret(secret_name: str, default: str | None = None) -> str | None:
    """Retrieve a secret from Key Vault with caching.

    Falls back to environment variables if Key Vault is unavailable.

    Args:
        secret_name: Name of the secret in Key Vault
        default: Default value if secret not found

    Returns:
        Secret value or default
    """
    # Check cache first
    if secret_name in _secrets_cache:
        return _secrets_cache[secret_name]

    # Try Key Vault
    client = _get_client()
    if client:
        try:
            secret = client.get_secret(secret_name)
            value = secret.value
            _secrets_cache[secret_name] = value
            logger.debug(f"Retrieved secret '{secret_name}' from Key Vault")
            return value
        except AzureError as e:
            logger.warning(f"Failed to get secret '{secret_name}': {e}")

    # Fallback to environment variable
    env_value = os.getenv(secret_name.upper().replace("-", "_"), default)
    if env_value:
        logger.debug(f"Using env var for '{secret_name}'")
    return env_value


@lru_cache(maxsize=1)
def get_database_url() -> str | None:
    """Construct database URL from Key Vault secrets or environment.

    In production: Uses postgres-password from Key Vault + other env vars
    In development: Uses DATABASE_URL environment variable directly
    """
    # First check for direct DATABASE_URL (local dev)
    direct_url = os.getenv("DATABASE_URL")
    if direct_url:
        return direct_url

    # Production: Construct from Key Vault password + env config
    password = get_secret("postgres-password")
    if not password:
        return None

    host = os.getenv("POSTGRES_HOST", "valargen-db.postgres.database.azure.com")
    user = os.getenv("POSTGRES_USER", "valargenadmin")
    db = os.getenv("POSTGRES_DB", "valargen")
    port = os.getenv("POSTGRES_PORT", "5432")

    return f"postgresql://{user}:{password}@{host}:{port}/{db}?sslmode=require"


def load_secrets() -> dict[str, str | None]:
    """Pre-load all configured secrets at startup.

    Returns:
        Dictionary of secret names to values
    """
    secrets = {}
    for env_name, vault_name in SECRET_MAPPINGS.items():
        secrets[env_name] = get_secret(vault_name)
    return secrets


def clear_cache() -> None:
    """Clear the secrets cache. Useful for testing or rotation."""
    global _secrets_cache
    _secrets_cache = {}
    get_database_url.cache_clear()
