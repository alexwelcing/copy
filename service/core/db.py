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

    def save_lead(self, lead_data: Dict[str, Any]) -> str:
        """Save a new lead to Firestore."""
        leads_col = self.db.collection('leads')
        if "created_at" not in lead_data:
            lead_data["created_at"] = datetime.utcnow()
        
        update_time, doc_ref = leads_col.add(lead_data)
        return doc_ref.id

# Singleton
_db: Optional[FirestoreClient] = None

def get_db() -> FirestoreClient:
    global _db
    if _db is None:
        _db = FirestoreClient()
    return _db
