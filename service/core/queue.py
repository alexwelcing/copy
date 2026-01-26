import os
import json
from typing import Optional
from google.cloud import pubsub_v1
from google.oauth2 import service_account
from service.api.schemas import WorkRequest

class TaskQueue:
    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.getenv("GCP_PROJECT_ID")
        self.topic_name = "agency-work-queue"
        
        # Load credentials
        if os.path.exists("service.json"):
            self.credentials = service_account.Credentials.from_service_account_file("service.json")
            self.publisher = pubsub_v1.PublisherClient(credentials=self.credentials)
            if not self.project_id:
                self.project_id = self.credentials.project_id
        else:
            self.publisher = pubsub_v1.PublisherClient()
            if not self.project_id:
                # Attempt to get project ID from default credentials or env
                self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

        if not self.project_id:
             # Fallback for local dev without strict setup
             print("Warning: No Project ID found for TaskQueue. Async tasks may fail.")

        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_name) if self.project_id else None

    def publish_task(self, request: WorkRequest, job_id: str) -> str:
        """
        Publish a work request to the queue.
        Returns the message ID.
        """
        if not self.topic_path:
            raise ValueError("TaskQueue not initialized with Project ID")

        # Create payload
        payload = {
            "job_id": job_id,
            "request": request.model_dump()
        }
        data = json.dumps(payload).encode("utf-8")
        
        future = self.publisher.publish(self.topic_path, data)
        return future.result()

# Singleton
_queue: Optional[TaskQueue] = None

def get_queue() -> TaskQueue:
    global _queue
    if _queue is None:
        _queue = TaskQueue()
    return _queue
