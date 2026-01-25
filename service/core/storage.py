import os
from datetime import timedelta
from typing import Optional
from google.cloud import storage
from google.oauth2 import service_account

class CloudStorage:
    def __init__(self, bucket_name: str = "marketing-copy-assets"):
        self.bucket_name = bucket_name
        
        # Load credentials from service.json if it exists
        if os.path.exists("service.json"):
            self.credentials = service_account.Credentials.from_service_account_file("service.json")
            self.client = storage.Client(credentials=self.credentials, project=self.credentials.project_id)
        else:
            self.client = storage.Client()
            
        self.bucket = self.client.bucket(bucket_name)

    def upload_file(self, local_path: str, destination_blob_name: str) -> str:
        """Uploads a file to the bucket."""
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_path)
        return blob.public_url

    def get_signed_url(self, blob_name: str, expiration_minutes: int = 60) -> str:
        """Generates a v4 signed URL for a blob."""
        blob = self.bucket.blob(blob_name)
        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=expiration_minutes),
            method="GET",
        )
        return url

    def list_assets(self, prefix: Optional[str] = None):
        """Lists all the blobs in the bucket."""
        blobs = self.client.list_blobs(self.bucket_name, prefix=prefix)
        return [{"name": blob.name, "url": self.get_signed_url(blob.name)} for blob in blobs]

# Singleton
_storage: Optional[CloudStorage] = None

def get_storage() -> CloudStorage:
    global _storage
    if _storage is None:
        _storage = CloudStorage()
    return _storage
