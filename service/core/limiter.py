from datetime import datetime
from typing import Optional
from service.core.db import get_db

class RateLimiter:
    def __init__(self):
        self.db = get_db()
        self.daily_limit_user = 5
        self.daily_limit_anon = 1

    def check_limit(self, user_id: str, is_anonymous: bool) -> bool:
        """
        Check if the user has exceeded their daily limit.
        Returns True if allowed, False if limit exceeded.
        """
        today = datetime.utcnow().strftime("%Y-%m-%d")
        
        # Collection path: users/{user_id}/usage/{date}
        # For anonymous: use a special prefix or collection? 
        # Let's treat anon IDs as normal user IDs but enforce lower limit.
        
        usage_ref = self.db.db.collection('users').document(user_id).collection('usage').document(today)
        
        # Atomic transaction to check and increment
        # Note: In a high-throughput scenario, we'd use a distributed counter or Redis.
        # For "5 per day", simple read-update is fine or even just Firestore increment.
        
        try:
            doc = usage_ref.get()
            current_count = 0
            if doc.exists:
                current_count = doc.to_dict().get("count", 0)
            
            limit = self.daily_limit_anon if is_anonymous else self.daily_limit_user
            
            if current_count >= limit:
                return False
                
            # Increment
            usage_ref.set({"count": current_count + 1}, merge=True)
            return True
            
        except Exception as e:
            print(f"Rate limiter error: {e}")
            # Fail open if DB error? Or fail closed? 
            # Let's fail open to not block users on infra glitches
            return True

_limiter: Optional[RateLimiter] = None

def get_limiter() -> RateLimiter:
    global _limiter
    if _limiter is None:
        _limiter = RateLimiter()
    return _limiter
