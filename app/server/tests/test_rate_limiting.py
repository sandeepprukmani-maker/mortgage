from services.rate_limit_service import RateLimitService


class TestRateLimitService:
    """Test suite for rate limiting service."""

    def test_check_rate_limit_allows_under_threshold(self, mock_redis):
        """Test rate limit allows requests under threshold."""
        rate_limit_service = RateLimitService(mock_redis)
        mock_redis.get.return_value = b'3'  # 3 attempts

        is_locked, attempts = rate_limit_service.check_rate_limit("test@example.com")

        assert is_locked is False
        assert attempts == 2  # 5 - 3 = 2 remaining

    def test_check_rate_limit_blocks_after_threshold(self, mock_redis):
        """Test rate limit blocks after threshold exceeded."""
        rate_limit_service = RateLimitService(mock_redis)
        mock_redis.get.return_value = b'5'  # 5 attempts (threshold)

        is_locked, attempts = rate_limit_service.check_rate_limit("test@example.com")

        assert is_locked is True
        assert attempts == 0

    def test_check_rate_limit_returns_correct_remaining_attempts(self, mock_redis):
        """Test rate limit returns correct remaining attempts."""
        rate_limit_service = RateLimitService(mock_redis)

        test_cases = [
            (0, 5),  # No attempts, 5 remaining
            (1, 4),  # 1 attempt, 4 remaining
            (2, 3),  # 2 attempts, 3 remaining
            (4, 1),  # 4 attempts, 1 remaining
        ]

        for attempts_count, expected_remaining in test_cases:
            mock_redis.get.return_value = str(attempts_count).encode() if attempts_count > 0 else None
            is_locked, remaining = rate_limit_service.check_rate_limit("test@example.com")
            assert remaining == expected_remaining

    def test_increment_failed_attempts_increases_counter(self, mock_redis):
        """Test incrementing failed attempts increases counter."""
        rate_limit_service = RateLimitService(mock_redis)
        mock_redis.get.return_value = "1"  # Simulate existing counter
        mock_redis.incr.return_value = 2

        rate_limit_service.increment_failed_attempts("test@example.com")

        mock_redis.incr.assert_called_once()

    def test_increment_failed_attempts_sets_expiry(self, mock_redis):
        """Test incrementing failed attempts sets expiry time."""
        rate_limit_service = RateLimitService(mock_redis)
        mock_redis.get.return_value = "4"  # Simulate 4 attempts already
        mock_redis.incr.return_value = 5  # This will be the 5th attempt (max)

        rate_limit_service.increment_failed_attempts("test@example.com")

        # Check that expire was called with lockout duration (900 seconds = 15 minutes)
        assert mock_redis.expire.called

    def test_reset_failed_attempts_deletes_key(self, mock_redis):
        """Test resetting failed attempts deletes Redis key."""
        rate_limit_service = RateLimitService(mock_redis)

        rate_limit_service.reset_failed_attempts("test@example.com")

        mock_redis.delete.assert_called_once()

    def test_rate_limit_with_different_identifiers(self, mock_redis):
        """Test rate limiting works independently for different identifiers."""
        rate_limit_service = RateLimitService(mock_redis)

        # Simulate different counters for different emails
        def get_side_effect(key):
            if 'user1' in key:
                return '3'
            elif 'user2' in key:
                return '1'
            return None

        mock_redis.get.side_effect = get_side_effect

        is_locked1, attempts1 = rate_limit_service.check_rate_limit("user1@example.com")
        is_locked2, attempts2 = rate_limit_service.check_rate_limit("user2@example.com")

        assert is_locked1 is False
        assert attempts1 == 2  # 5 - 3
        assert is_locked2 is False
        assert attempts2 == 4  # 5 - 1

    def test_check_rate_limit_with_no_attempts(self, mock_redis):
        """Test rate limit check when no previous attempts exist."""
        rate_limit_service = RateLimitService(mock_redis)
        mock_redis.get.return_value = None

        is_locked, attempts = rate_limit_service.check_rate_limit("new@example.com")

        assert is_locked is False
        assert attempts == 5  # All 5 attempts available

    def test_lockout_duration_is_fifteen_minutes(self, mock_redis):
        """Test lockout duration is 15 minutes (900 seconds)."""
        rate_limit_service = RateLimitService(mock_redis)
        mock_redis.get.return_value = "4"  # Simulate 4 attempts already
        mock_redis.incr.return_value = 5  # This will be the 5th attempt (max)

        rate_limit_service.increment_failed_attempts("test@example.com")

        # Check that expire was called with 900 seconds
        call_args = mock_redis.expire.call_args
        assert call_args is not None
        assert 900 in call_args[0] or 900 in call_args[1].values()
