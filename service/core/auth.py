import logging
import os
import firebase_admin
from firebase_admin import auth, credentials
from fastapi import HTTPException, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

# Initialize Firebase Admin
# Check if already initialized to avoid errors during reloads
if not firebase_admin._apps:
    if os.path.exists("service.json"):
        cred = credentials.Certificate("service.json")
        firebase_admin.initialize_app(cred)
    else:
        # Implicit credentials (GCP environment)
        firebase_admin.initialize_app()

security = HTTPBearer(auto_error=False)

async def get_current_user(
    request: Request,
    token: Optional[HTTPAuthorizationCredentials] = Security(security)
) -> Tuple[str, bool]:
    """
    Verify Firebase Token or Anonymous ID.
    Returns (user_id, is_anonymous).
    """
    
    # 1. Check for valid Firebase Token
    if token and token.credentials:
        try:
            decoded_token = auth.verify_id_token(token.credentials)
            uid = decoded_token['uid']
            return uid, False
        except Exception as e:
            # Invalid token
            logger.debug(f"Firebase token verification failed: {e}")
            pass # Fallthrough to check for anon
            
    # 2. Check for Anonymous ID (Cookie or Header)
    # Support standard Segment-style cookie or our custom header
    anon_id = request.cookies.get("ajs_anonymous_id") or request.headers.get("X-Anonymous-ID")
    
    if anon_id:
        # Normalize: ensure it's a string and strip quotes if from cookie
        anon_id = str(anon_id).strip('"')
        logger.debug(f"Authenticated as anonymous user: {anon_id}")
        return f"anon_{anon_id}", True
        
    logger.warning(f"Authentication failed for request to {request.url.path}")
    raise HTTPException(
        status_code=401,
        detail="Authentication required. Please sign in or provide anonymous ID."
    )
