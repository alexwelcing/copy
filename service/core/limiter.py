from datetime import datetime
from typing import Optional
from service.core.db import get_db

class RateLimiter:
    def __init__(self):
        self.db = get_db()
        self.daily_limit_anon = 1
        self.daily_limit_user = 5  # default for free plan

        # Plan-specific daily limits
        self.plan_daily_limits = {
            "free": 5,
            "starter": 100,
            "growth": 500,
            "enterprise": 2000,
        }

    def check_limit(self, user_id: str, is_anonymous: bool) -> tuple[bool, int]:
        """
        Check if the user has exceeded their daily limit.
        Returns (is_allowed, current_count).
        """
        today = datetime.utcnow().strftime("%Y-%m-%d")

        usage_ref = self.db.db.collection('users').document(user_id).collection('usage').document(today)

        try:
            doc = usage_ref.get()
            current_count = 0
            if doc.exists:
                current_count = doc.to_dict().get("count", 0)

            if is_anonymous:
                limit = self.daily_limit_anon
            else:
                # Look up tenant plan for authenticated users
                limit = self.daily_limit_user
                try:
                    tenant = self.db.get_tenant_by_user(user_id)
                    if tenant:
                        plan = tenant.get("plan", "free")
                        limit = self.plan_daily_limits.get(plan, self.daily_limit_user)
                except Exception:
                    pass  # Fall back to default if tenant lookup fails

            if current_count >= limit:
                return False, current_count

            # Increment
            usage_ref.set({"count": current_count + 1}, merge=True)
            return True, current_count + 1

        except Exception as e:
            print(f"Rate limiter error: {e}")
            # Fail open to not block users on infra glitches
            return True, 0

_limiter: Optional[RateLimiter] = None

def get_limiter() -> RateLimiter:
    global _limiter
    if _limiter is None:
        _limiter = RateLimiter()
    return _limiter
