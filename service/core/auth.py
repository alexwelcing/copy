import os
import firebase_admin
from firebase_admin import auth, credentials
from fastapi import HTTPException, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Tuple

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
            print(f"Auth error: {e}")
            pass # Fallthrough to check for anon
            
    # 2. Check for Anonymous ID header
    anon_id = request.headers.get("X-Anonymous-ID")
    if anon_id:
        # Prefix to avoid collision with real UIDs
        return f"anon_{anon_id}", True
        
    raise HTTPException(
        status_code=401,
        detail="Authentication required. Please sign in or provide anonymous ID."
    )
