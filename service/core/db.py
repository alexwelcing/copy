import os
from typing import Optional, List, Dict, Any
from google.cloud import firestore
from google.oauth2 import service_account
from datetime import datetime

class FirestoreClient:
    def __init__(self, project_id: Optional[str] = None):
        # Load credentials from service.json if it exists
        if os.path.exists("service.json"):
            self.credentials = service_account.Credentials.from_service_account_file("service.json")
            self.db = firestore.Client(credentials=self.credentials, project=self.credentials.project_id)
        else:
            # Fallback to default credentials (works in Cloud Run)
            self.db = firestore.Client(project=project_id)

        self.briefs_collection = self.db.collection('briefs')

    def check_connectivity(self) -> bool:
        """Test Firestore connectivity with a lightweight read."""
        try:
            # Limit 1 is the cheapest possible query
            list(self.briefs_collection.limit(1).stream())
            return True
        except Exception:
            return False

    def save_brief(self, brief_data: Dict[str, Any]) -> str:
        """
        Save a brief to Firestore.
        Returns the document ID.
        """
        # Add metadata
        if "created_at" not in brief_data:
            brief_data["created_at"] = datetime.utcnow()
        brief_data["updated_at"] = datetime.utcnow()

        if "id" in brief_data and brief_data["id"]:
            doc_ref = self.briefs_collection.document(brief_data["id"])
            doc_ref.set(brief_data, merge=True)
            return brief_data["id"]
        else:
            update_time, doc_ref = self.briefs_collection.add(brief_data)
            return doc_ref.id

    def get_brief(self, brief_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a brief by ID."""
        doc = self.briefs_collection.document(brief_id).get()
        if doc.exists:
            data = doc.to_dict()
            data["id"] = doc.id
            return data
        return None

    def list_briefs(self, limit: int = 20) -> List[Dict[str, Any]]:
        """List recent briefs."""
        docs = self.briefs_collection.order_by(
            "updated_at", direction=firestore.Query.DESCENDING
        ).limit(limit).stream()
        
        results = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            results.append(data)
        return results

    def get_brief_by_anonymous_id(self, anon_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve most recent brief for an anonymous ID."""
        docs = self.briefs_collection.where(
            "anonymous_id", "==", anon_id
        ).order_by("created_at", direction=firestore.Query.DESCENDING).limit(1).get()
        
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            return data
        return None

    def claim_anonymous_work(self, anon_id: str, user_id: str):
        """Reassign all briefs and profiles from an anonymous ID to a real user ID."""
        # 1. Claim Briefs
        brief_docs = self.briefs_collection.where("anonymous_id", "==", anon_id).get()
        for doc in brief_docs:
            doc.reference.update({
                "user_id": user_id,
                "anonymous_id": firestore.DELETE_FIELD,
                "claimed_at": datetime.utcnow()
            })

        # 2. Claim Profile (if exists)
        anon_profile = self.db.collection('users').document(anon_id).get()
        if anon_profile.exists:
            profile_data = anon_profile.to_dict()
            # Merge into real user profile
            self.save_user_profile(user_id, profile_data)
            # Delete anon profile
            anon_profile.reference.delete()

    def save_lead(self, lead_data: Dict[str, Any]) -> str:
        """Save a new lead to Firestore."""
        leads_col = self.db.collection('leads')
        if "created_at" not in lead_data:
            lead_data["created_at"] = datetime.utcnow()
        
        update_time, doc_ref = leads_col.add(lead_data)
        return doc_ref.id

    def save_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> str:
        """Save or update a user profile."""
        users_col = self.db.collection('users')
        doc_ref = users_col.document(user_id)
        
        profile_data["updated_at"] = datetime.utcnow()
        if "created_at" not in profile_data:
            # Check if exists to preserve created_at or set new
            doc = doc_ref.get()
            if not doc.exists:
                profile_data["created_at"] = datetime.utcnow()
        
        doc_ref.set(profile_data, merge=True)
        return user_id

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a user profile."""
        doc = self.db.collection('users').document(user_id).get()
        if doc.exists:
            return doc.to_dict()
        return None

    # =========================================================================
    # Tenant Management
    # =========================================================================

    def get_tenant_by_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get tenant by Firebase user_id."""
        docs = self.db.collection('tenants').where(
            "user_id", "==", user_id
        ).limit(1).get()
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            return data
        return None

    def get_or_create_tenant(self, user_id: str, email: str = "") -> Dict[str, Any]:
        """Get tenant by user_id, or create a free-tier tenant."""
        existing = self.get_tenant_by_user(user_id)
        if existing:
            return existing

        tenant_data = {
            "user_id": user_id,
            "email": email,
            "plan": "free",
            "billing": {"status": "active"},
            "limits": {
                "tokens_per_period": 50000,
                "sprites_per_period": 5,
                "max_concurrent_sprites": 1,
            },
            "usage": {
                "tokens_this_period": 0,
                "sprites_spawned_this_period": 0,
                "api_calls_this_period": 0,
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        _, doc_ref = self.db.collection('tenants').add(tenant_data)
        tenant_data["id"] = doc_ref.id
        return tenant_data

    def get_tenant_by_stripe_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Lookup tenant by stripe_customer_id for webhook processing."""
        docs = self.db.collection('tenants').where(
            "billing.stripe_customer_id", "==", customer_id
        ).limit(1).get()
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            return data
        return None

    def get_tenant(self, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Get tenant by document ID."""
        doc = self.db.collection('tenants').document(tenant_id).get()
        if doc.exists:
            data = doc.to_dict()
            data["id"] = doc.id
            return data
        return None

    def update_tenant(self, tenant_id: str, updates: Dict[str, Any]):
        """Update tenant fields."""
        updates["updated_at"] = datetime.utcnow()
        self.db.collection('tenants').document(tenant_id).update(updates)

# Singleton
_db: Optional[FirestoreClient] = None

def get_db() -> FirestoreClient:
    global _db
    if _db is None:
        _db = FirestoreClient()
    return _db
