"""
Tests for OAuth service.
"""
import pytest
from unittest.mock import patch, Mock, AsyncMock
import httpx

from services.oauth_service import OAuthService, GOOGLE_ERROR_MESSAGES


class TestOAuthServiceConfiguration:
    """Tests for OAuth service configuration validation."""

    def test_is_configured_returns_true_when_credentials_set(self):
        """Test is_configured returns True when both credentials are set."""
        with patch('services.oauth_service.settings') as mock_settings:
            mock_settings.google_client_id = "test-client-id"
            mock_settings.google_client_secret = "test-client-secret"
            mock_settings.google_redirect_uri = "http://localhost:8000/callback"

            service = OAuthService()
            assert service.is_configured() is True

    def test_is_configured_returns_false_when_client_id_missing(self):
        """Test is_configured returns False when client_id is missing."""
        with patch('services.oauth_service.settings') as mock_settings:
            mock_settings.google_client_id = ""
            mock_settings.google_client_secret = "test-client-secret"
            mock_settings.google_redirect_uri = "http://localhost:8000/callback"

            service = OAuthService()
            assert service.is_configured() is False

    def test_is_configured_returns_false_when_client_secret_missing(self):
        """Test is_configured returns False when client_secret is missing."""
        with patch('services.oauth_service.settings') as mock_settings:
            mock_settings.google_client_id = "test-client-id"
            mock_settings.google_client_secret = ""
            mock_settings.google_redirect_uri = "http://localhost:8000/callback"

            service = OAuthService()
            assert service.is_configured() is False

    def test_is_configured_returns_false_when_both_missing(self):
        """Test is_configured returns False when both credentials are missing."""
        with patch('services.oauth_service.settings') as mock_settings:
            mock_settings.google_client_id = ""
            mock_settings.google_client_secret = ""
            mock_settings.google_redirect_uri = "http://localhost:8000/callback"

            service = OAuthService()
            assert service.is_configured() is False


class TestOAuthServiceValidation:
    """Tests for OAuth credential validation."""

    def test_validate_credentials_passes_when_configured(self):
        """Test validate_credentials doesn't raise when credentials are set."""
        with patch('services.oauth_service.settings') as mock_settings:
            mock_settings.google_client_id = "test-client-id"
            mock_settings.google_client_secret = "test-client-secret"
            mock_settings.google_redirect_uri = "http://localhost:8000/callback"

            service = OAuthService()
            # Should not raise
            service.validate_credentials()

    def test_validate_credentials_raises_when_client_id_missing(self):
        """Test validate_credentials raises ValueError when client_id is missing."""
        with patch('services.oauth_service.settings') as mock_settings:
            mock_settings.google_client_id = ""
            mock_settings.google_client_secret = "test-client-secret"
            mock_settings.google_redirect_uri = "http://localhost:8000/callback"

            service = OAuthService()
            with pytest.raises(ValueError) as exc_info:
                service.validate_credentials()
            assert "GOOGLE_CLIENT_ID" in str(exc_info.value)

    def test_validate_credentials_raises_when_client_secret_missing(self):
        """Test validate_credentials raises ValueError when client_secret is missing."""
        with patch('services.oauth_service.settings') as mock_settings:
            mock_settings.google_client_id = "test-client-id"
            mock_settings.google_client_secret = ""
            mock_settings.google_redirect_uri = "http://localhost:8000/callback"

            service = OAuthService()
            with pytest.raises(ValueError) as exc_info:
                service.validate_credentials()
            assert "GOOGLE_CLIENT_SECRET" in str(exc_info.value)


class TestOAuthServiceAuthorizationUrl:
    """Tests for authorization URL generation."""

    def test_get_authorization_url_includes_required_params(self):
        """Test get_google_authorization_url includes all required parameters."""
        with patch('services.oauth_service.settings') as mock_settings:
            mock_settings.google_client_id = "test-client-id"
            mock_settings.google_client_secret = "test-client-secret"
            mock_settings.google_redirect_uri = "http://localhost:8000/callback"

            service = OAuthService()
            url = service.get_google_authorization_url()

            assert "client_id=test-client-id" in url
            assert "redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fcallback" in url
            assert "response_type=code" in url
            assert "scope=openid+email+profile" in url

    def test_get_authorization_url_raises_when_not_configured(self):
        """Test get_google_authorization_url raises when credentials not configured."""
        with patch('services.oauth_service.settings') as mock_settings:
            mock_settings.google_client_id = ""
            mock_settings.google_client_secret = ""
            mock_settings.google_redirect_uri = "http://localhost:8000/callback"

            service = OAuthService()
            with pytest.raises(ValueError) as exc_info:
                service.get_google_authorization_url()
            assert "not configured" in str(exc_info.value)


class TestOAuthServiceErrorParsing:
    """Tests for Google OAuth error parsing."""

    def test_parse_google_error_invalid_client(self):
        """Test parsing invalid_client error from Google."""
        with patch('services.oauth_service.settings') as mock_settings:
            mock_settings.google_client_id = "test-client-id"
            mock_settings.google_client_secret = "test-client-secret"
            mock_settings.google_redirect_uri = "http://localhost:8000/callback"

            service = OAuthService()

            mock_response = Mock()
            mock_response.json.return_value = {
                "error": "invalid_client",
                "error_description": "The OAuth client was not found."
            }
            mock_response.status_code = 401

            error_message = service._parse_google_error(mock_response)
            assert "Invalid Google OAuth credentials" in error_message

    def test_parse_google_error_invalid_grant(self):
        """Test parsing invalid_grant error from Google."""
        with patch('services.oauth_service.settings') as mock_settings:
            mock_settings.google_client_id = "test-client-id"
            mock_settings.google_client_secret = "test-client-secret"
            mock_settings.google_redirect_uri = "http://localhost:8000/callback"

            service = OAuthService()

            mock_response = Mock()
            mock_response.json.return_value = {
                "error": "invalid_grant",
                "error_description": "Code was already redeemed."
            }
            mock_response.status_code = 400

            error_message = service._parse_google_error(mock_response)
            assert "expired or already used" in error_message

    def test_parse_google_error_redirect_uri_mismatch(self):
        """Test parsing redirect_uri_mismatch error from Google."""
        with patch('services.oauth_service.settings') as mock_settings:
            mock_settings.google_client_id = "test-client-id"
            mock_settings.google_client_secret = "test-client-secret"
            mock_settings.google_redirect_uri = "http://localhost:8000/callback"

            service = OAuthService()

            mock_response = Mock()
            mock_response.json.return_value = {
                "error": "redirect_uri_mismatch",
                "error_description": "Bad Request"
            }
            mock_response.status_code = 400

            error_message = service._parse_google_error(mock_response)
            assert "redirect URI mismatch" in error_message

    def test_parse_google_error_unknown_error(self):
        """Test parsing unknown error from Google."""
        with patch('services.oauth_service.settings') as mock_settings:
            mock_settings.google_client_id = "test-client-id"
            mock_settings.google_client_secret = "test-client-secret"
            mock_settings.google_redirect_uri = "http://localhost:8000/callback"

            service = OAuthService()

            mock_response = Mock()
            mock_response.json.return_value = {
                "error": "unknown_error_code",
                "error_description": "Something went wrong"
            }
            mock_response.status_code = 400

            error_message = service._parse_google_error(mock_response)
            assert "Something went wrong" in error_message

    def test_parse_google_error_malformed_response(self):
        """Test parsing malformed error response from Google."""
        with patch('services.oauth_service.settings') as mock_settings:
            mock_settings.google_client_id = "test-client-id"
            mock_settings.google_client_secret = "test-client-secret"
            mock_settings.google_redirect_uri = "http://localhost:8000/callback"

            service = OAuthService()

            mock_response = Mock()
            mock_response.json.side_effect = Exception("Invalid JSON")
            mock_response.status_code = 500

            error_message = service._parse_google_error(mock_response)
            assert "status 500" in error_message


class TestOAuthServiceTokenExchange:
    """Tests for token exchange functionality."""

    @pytest.mark.asyncio
    async def test_exchange_code_raises_when_not_configured(self):
        """Test exchange_code_for_token raises when credentials not configured."""
        with patch('services.oauth_service.settings') as mock_settings:
            mock_settings.google_client_id = ""
            mock_settings.google_client_secret = ""
            mock_settings.google_redirect_uri = "http://localhost:8000/callback"

            service = OAuthService()
            with pytest.raises(ValueError) as exc_info:
                await service.exchange_code_for_token("test-code")
            assert "not configured" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_exchange_code_success(self):
        """Test successful token exchange."""
        with patch('services.oauth_service.settings') as mock_settings:
            mock_settings.google_client_id = "test-client-id"
            mock_settings.google_client_secret = "test-client-secret"
            mock_settings.google_redirect_uri = "http://localhost:8000/callback"

            service = OAuthService()

            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "access_token": "test-access-token",
                "token_type": "Bearer",
                "expires_in": 3600
            }

            with patch('httpx.AsyncClient') as mock_client:
                mock_instance = AsyncMock()
                mock_instance.post.return_value = mock_response
                mock_client.return_value.__aenter__.return_value = mock_instance

                result = await service.exchange_code_for_token("test-code")

                assert result["access_token"] == "test-access-token"
                assert result["token_type"] == "Bearer"

    @pytest.mark.asyncio
    async def test_exchange_code_handles_401_error(self):
        """Test token exchange handles 401 error from Google."""
        with patch('services.oauth_service.settings') as mock_settings:
            mock_settings.google_client_id = "test-client-id"
            mock_settings.google_client_secret = "test-client-secret"
            mock_settings.google_redirect_uri = "http://localhost:8000/callback"

            service = OAuthService()

            mock_response = Mock()
            mock_response.status_code = 401
            mock_response.json.return_value = {
                "error": "invalid_client",
                "error_description": "The OAuth client was not found."
            }

            with patch('httpx.AsyncClient') as mock_client:
                mock_instance = AsyncMock()
                mock_instance.post.return_value = mock_response
                mock_client.return_value.__aenter__.return_value = mock_instance

                with pytest.raises(ValueError) as exc_info:
                    await service.exchange_code_for_token("test-code")

                assert "Invalid Google OAuth credentials" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_exchange_code_handles_network_error(self):
        """Test token exchange handles network errors."""
        with patch('services.oauth_service.settings') as mock_settings:
            mock_settings.google_client_id = "test-client-id"
            mock_settings.google_client_secret = "test-client-secret"
            mock_settings.google_redirect_uri = "http://localhost:8000/callback"

            service = OAuthService()

            with patch('httpx.AsyncClient') as mock_client:
                mock_instance = AsyncMock()
                mock_instance.post.side_effect = httpx.RequestError("Connection failed")
                mock_client.return_value.__aenter__.return_value = mock_instance

                with pytest.raises(ValueError) as exc_info:
                    await service.exchange_code_for_token("test-code")

                assert "Unable to connect" in str(exc_info.value)


class TestGoogleErrorMessages:
    """Tests for Google error message mappings."""

    def test_all_expected_error_codes_mapped(self):
        """Test that all expected Google error codes have mappings."""
        expected_codes = [
            "invalid_client",
            "invalid_grant",
            "redirect_uri_mismatch",
            "unauthorized_client",
            "access_denied",
            "invalid_request"
        ]
        for code in expected_codes:
            assert code in GOOGLE_ERROR_MESSAGES
            assert len(GOOGLE_ERROR_MESSAGES[code]) > 0
