import pytest
from services.password_service import PasswordService


class TestPasswordService:
    """Test suite for password service."""

    def setup_method(self):
        """Setup test password service."""
        self.password_service = PasswordService()

    def test_hash_password_creates_different_hashes(self):
        """Test that hashing the same password twice produces different hashes."""
        password = "TestPassword123"
        hash1 = self.password_service.hash_password(password)
        hash2 = self.password_service.hash_password(password)

        assert hash1 != hash2
        assert hash1 is not None
        assert hash2 is not None

    def test_verify_password_succeeds_with_correct_password(self):
        """Test password verification succeeds with correct password."""
        password = "TestPassword123"
        password_hash = self.password_service.hash_password(password)

        assert self.password_service.verify_password(password, password_hash) is True

    def test_verify_password_fails_with_incorrect_password(self):
        """Test password verification fails with incorrect password."""
        password = "TestPassword123"
        wrong_password = "WrongPassword123"
        password_hash = self.password_service.hash_password(password)

        assert self.password_service.verify_password(wrong_password, password_hash) is False

    def test_validate_password_strength_accepts_valid_password(self):
        """Test password validation accepts strong passwords."""
        valid_passwords = [
            "Password1",
            "Test1234",
            "Secure123",
            "MyPassword9",
            "ValidPass1"
        ]

        for password in valid_passwords:
            result = self.password_service.validate_password_strength(password)
            assert result is True

    def test_validate_password_strength_rejects_short_password(self):
        """Test password validation rejects passwords shorter than 8 characters."""
        with pytest.raises(ValueError) as exc_info:
            self.password_service.validate_password_strength("Pass1")

        assert "at least 8 characters" in str(exc_info.value)

    def test_validate_password_strength_rejects_no_uppercase(self):
        """Test password validation rejects passwords without uppercase letters."""
        with pytest.raises(ValueError) as exc_info:
            self.password_service.validate_password_strength("password123")

        assert "uppercase letter" in str(exc_info.value)

    def test_validate_password_strength_rejects_no_number(self):
        """Test password validation rejects passwords without numbers."""
        with pytest.raises(ValueError) as exc_info:
            self.password_service.validate_password_strength("Password")

        assert "number" in str(exc_info.value)

    def test_validate_password_strength_rejects_empty_password(self):
        """Test password validation rejects empty passwords."""
        with pytest.raises(ValueError):
            self.password_service.validate_password_strength("")

    def test_hash_password_with_special_characters(self):
        """Test hashing passwords with special characters."""
        password = "P@ssw0rd!"
        password_hash = self.password_service.hash_password(password)

        assert self.password_service.verify_password(password, password_hash) is True

    def test_verify_password_case_sensitive(self):
        """Test password verification is case-sensitive."""
        password = "TestPassword123"
        password_hash = self.password_service.hash_password(password)

        assert self.password_service.verify_password("testpassword123", password_hash) is False
        assert self.password_service.verify_password("TESTPASSWORD123", password_hash) is False
