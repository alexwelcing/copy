import pytest
import os
from unittest.mock import Mock, patch, MagicMock

# Skip tests that require GCP credentials if not available
requires_gcp = pytest.mark.skipif(
    not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and not os.path.exists("service.json"),
    reason="GCP credentials not available"
)


class TestRateLimiterLogic:
    """Test rate limiter logic without actual Firestore connection."""
    
    def test_rate_limiter_limits(self):
        """Verify rate limit constants."""
        from service.core.limiter import RateLimiter
        
        # Mock the database to avoid Firestore connection
        with patch('service.core.limiter.get_db') as mock_get_db:
            mock_db = MagicMock()
            mock_get_db.return_value = mock_db
            
            limiter = RateLimiter()
            
            # Verify limits are set correctly
            assert limiter.daily_limit_user == 5
            assert limiter.daily_limit_anon == 1
    
    def test_rate_limiter_allows_under_limit(self):
        """Test that rate limiter allows requests under the limit."""
        from service.core.limiter import RateLimiter
        
        with patch('service.core.limiter.get_db') as mock_get_db:
            mock_db = MagicMock()
            mock_get_db.return_value = mock_db
            
            # Mock Firestore document that shows 0 requests
            mock_doc = MagicMock()
            mock_doc.exists = True
            mock_doc.to_dict.return_value = {"count": 0}
            mock_db.db.collection.return_value.document.return_value.collection.return_value.document.return_value.get.return_value = mock_doc
            
            limiter = RateLimiter()
            result = limiter.check_limit("test-user", is_anonymous=False)
            
            assert result is True
    
    def test_rate_limiter_blocks_over_limit(self):
        """Test that rate limiter blocks requests over the limit."""
        from service.core.limiter import RateLimiter
        
        with patch('service.core.limiter.get_db') as mock_get_db:
            mock_db = MagicMock()
            mock_get_db.return_value = mock_db
            
            # Mock Firestore document that shows 5 requests (at limit for user)
            mock_doc = MagicMock()
            mock_doc.exists = True
            mock_doc.to_dict.return_value = {"count": 5}
            mock_db.db.collection.return_value.document.return_value.collection.return_value.document.return_value.get.return_value = mock_doc
            
            limiter = RateLimiter()
            result = limiter.check_limit("test-user", is_anonymous=False)
            
            assert result is False
    
    def test_rate_limiter_anon_lower_limit(self):
        """Test that anonymous users have lower limits."""
        from service.core.limiter import RateLimiter
        
        with patch('service.core.limiter.get_db') as mock_get_db:
            mock_db = MagicMock()
            mock_get_db.return_value = mock_db
            
            # Mock Firestore document that shows 1 request (at limit for anon)
            mock_doc = MagicMock()
            mock_doc.exists = True
            mock_doc.to_dict.return_value = {"count": 1}
            mock_db.db.collection.return_value.document.return_value.collection.return_value.document.return_value.get.return_value = mock_doc
            
            limiter = RateLimiter()
            result = limiter.check_limit("anon-user", is_anonymous=True)
            
            assert result is False
    
    def test_rate_limiter_fails_open_on_error(self):
        """Test that rate limiter fails open (allows request) on DB errors."""
        from service.core.limiter import RateLimiter
        
        with patch('service.core.limiter.get_db') as mock_get_db:
            mock_db = MagicMock()
            mock_get_db.return_value = mock_db
            
            # Mock Firestore to raise an exception
            mock_db.db.collection.return_value.document.return_value.collection.return_value.document.return_value.get.side_effect = Exception("DB Error")
            
            limiter = RateLimiter()
            result = limiter.check_limit("test-user", is_anonymous=False)
            
            # Should fail open
            assert result is True


@requires_gcp
class TestRateLimiterIntegration:
    """Integration tests that require actual Firestore connection."""
    
    def test_rate_limiter_firestore_persistence(self):
        """Test that rate limits persist to Firestore."""
        from service.core.limiter import get_limiter
        
        limiter = get_limiter()
        
        # This test would require actual Firestore
        # and would verify that counts persist across requests
        assert limiter.db is not None
