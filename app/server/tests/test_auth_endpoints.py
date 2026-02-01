

class TestAuthEndpoints:
    """Integration tests for authentication endpoints."""

    def test_register_creates_user(self, client, db_session, test_tenant, test_role):
        """Test user registration creates new user."""
        response = client.post("/api/auth/register", json={
            "email": "newuser@example.com",
            "password": "NewUser123",
            "first_name": "New",
            "last_name": "User"
        })

        assert response.status_code == 201
        data = response.json()
        assert "message" in data
        assert "successful" in data["message"].lower()

    def test_register_fails_with_duplicate_email(self, client, test_user):
        """Test registration fails with existing email."""
        response = client.post("/api/auth/register", json={
            "email": test_user.email,
            "password": "Password123",
            "first_name": "Test",
            "last_name": "User"
        })

        assert response.status_code == 409

    def test_register_fails_with_weak_password(self, client):
        """Test registration fails with weak password."""
        response = client.post("/api/auth/register", json={
            "email": "test@example.com",
            "password": "weak",
            "first_name": "Test",
            "last_name": "User"
        })

        assert response.status_code == 422  # Pydantic validation error

    def test_login_succeeds_with_correct_credentials(self, client, test_user):
        """Test login succeeds with valid credentials."""
        response = client.post("/api/auth/login", json={
            "email": test_user.email,
            "password": "Test1234"
        })

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_fails_with_incorrect_password(self, client, test_user):
        """Test login fails with wrong password."""
        response = client.post("/api/auth/login", json={
            "email": test_user.email,
            "password": "WrongPassword123"
        })

        assert response.status_code == 401

    def test_login_fails_with_nonexistent_email(self, client):
        """Test login fails with non-existent email."""
        response = client.post("/api/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "Password123"
        })

        assert response.status_code == 401

    def test_login_fails_for_google_user_with_password(self, client, test_google_user):
        """Test local login fails for Google OAuth users."""
        response = client.post("/api/auth/login", json={
            "email": test_google_user.email,
            "password": "Password123"
        })

        assert response.status_code == 400
        data = response.json()
        assert "google" in data["detail"].lower()

    def test_logout_revokes_refresh_token(self, client, test_user, test_refresh_token):
        """Test logout revokes refresh token."""
        # Set refresh token in cookie
        client.cookies.set("refresh_token", test_refresh_token.token)

        response = client.post("/api/auth/logout")

        assert response.status_code == 200

    def test_refresh_token_returns_new_access_token(self, client, test_refresh_token):
        """Test token refresh returns new access token."""
        client.cookies.set("refresh_token", test_refresh_token.token)

        response = client.post("/api/auth/refresh")

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    def test_refresh_token_fails_with_invalid_token(self, client):
        """Test refresh fails with invalid token."""
        client.cookies.set("refresh_token", "invalid-token")

        response = client.post("/api/auth/refresh")

        assert response.status_code == 401

    def test_get_current_user_succeeds_with_valid_token(self, authenticated_client, test_user):
        """Test fetching current user with valid token."""
        response = authenticated_client.get("/api/users/me")

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["first_name"] == test_user.first_name

    def test_get_current_user_fails_without_token(self, client):
        """Test fetching current user fails without token."""
        response = client.get("/api/users/me")

        assert response.status_code == 401

    def test_get_current_user_fails_with_invalid_token(self, client):
        """Test fetching current user fails with invalid token."""
        client.headers = {"Authorization": "Bearer invalid.token.here"}
        response = client.get("/api/users/me")

        assert response.status_code == 401

    def test_forgot_password_returns_success(self, client, test_user):
        """Test forgot password always returns success."""
        response = client.post("/api/auth/forgot-password", json={
            "email": test_user.email
        })

        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_forgot_password_with_nonexistent_email(self, client):
        """Test forgot password with non-existent email (still returns success)."""
        response = client.post("/api/auth/forgot-password", json={
            "email": "nonexistent@example.com"
        })

        assert response.status_code == 200

    def test_forgot_password_fails_for_google_user(self, client, test_google_user):
        """Test forgot password returns appropriate message for Google users."""
        response = client.post("/api/auth/forgot-password", json={
            "email": test_google_user.email
        })

        # Should still return success to prevent enumeration
        assert response.status_code == 200

    async def test_reset_password_succeeds_with_valid_token(self, client, db_session, test_user):
        """Test password reset succeeds with valid token."""
        from models.password_reset import PasswordResetToken
        from datetime import datetime, timedelta, timezone
        import uuid

        # Create a valid reset token
        reset_token = PasswordResetToken(
            token=str(uuid.uuid4()),
            user_id=test_user.id,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            is_used=False
        )
        db_session.add(reset_token)
        await db_session.commit()

        response = client.post("/api/auth/reset-password", json={
            "token": reset_token.token,
            "new_password": "NewPassword123"
        })

        assert response.status_code == 200

    async def test_reset_password_fails_with_expired_token(self, client, db_session, test_user):
        """Test password reset fails with expired token."""
        from models.password_reset import PasswordResetToken
        from datetime import datetime, timedelta, timezone
        import uuid

        # Create an expired reset token
        reset_token = PasswordResetToken(
            token=str(uuid.uuid4()),
            user_id=test_user.id,
            expires_at=datetime.now(timezone.utc) - timedelta(hours=1),
            is_used=False
        )
        db_session.add(reset_token)
        await db_session.commit()

        response = client.post("/api/auth/reset-password", json={
            "token": reset_token.token,
            "new_password": "NewPassword123"
        })

        assert response.status_code == 400

    async def test_reset_password_fails_with_used_token(self, client, db_session, test_user):
        """Test password reset fails with already used token."""
        from models.password_reset import PasswordResetToken
        from datetime import datetime, timedelta, timezone
        import uuid

        # Create a used reset token
        reset_token = PasswordResetToken(
            token=str(uuid.uuid4()),
            user_id=test_user.id,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            is_used=True
        )
        db_session.add(reset_token)
        await db_session.commit()

        response = client.post("/api/auth/reset-password", json={
            "token": reset_token.token,
            "new_password": "NewPassword123"
        })

        assert response.status_code == 400

    async def test_login_updates_last_login_timestamp(self, client, test_user, db_session):
        """Test successful login updates last_login_at timestamp."""
        import time

        original_last_login = test_user.last_login_at

        time.sleep(0.1)  # Small delay to ensure timestamp difference

        response = client.post("/api/auth/login", json={
            "email": test_user.email,
            "password": "Test1234"
        })

        assert response.status_code == 200

        await db_session.refresh(test_user)
        assert test_user.last_login_at != original_last_login
