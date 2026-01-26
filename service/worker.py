import os
import json
import time
from google.cloud import pubsub_v1
from google.oauth2 import service_account
from service.core.executor import get_executor
from service.core.db import get_db
from service.api.schemas import WorkRequest, WorkResult

def callback(message):
    print(f"Received message: {message.message_id}")
    try:
        data = json.loads(message.data.decode("utf-8"))
        job_id = data.get("job_id")
        request_data = data.get("request")
        
        if not job_id or not request_data:
            print("Invalid message format")
            message.ack()
            return

        request = WorkRequest(**request_data)
        
        # Update DB status to Processing
        db = get_db()
        db.save_brief({
            "id": job_id, 
            "status": "processing",
            "skill": request.skill.value # Store skill for reference
        })

        # Execute
        print(f"Executing skill: {request.skill}")
        executor = get_executor()
        result = executor.execute(request)
        
        # Update DB with result
        db.save_brief({
            "id": job_id,
            "status": "completed",
            "output": result.output,
            "sections": result.sections,
            "alternatives": result.alternatives,
            "recommendations": result.recommendations,
            "metadata": result.metadata
        })
        
        print(f"Job {job_id} completed.")
        message.ack()
        
    except Exception as e:
        print(f"Error processing message: {e}")
        # Update DB with error
        if 'job_id' in locals() and job_id:
             try:
                db = get_db()
                db.save_brief({"id": job_id, "status": "failed", "error": str(e)})
             except:
                 pass
        message.nack()

def main():
    project_id = os.getenv("GCP_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT")
    subscription_name = "agency-worker-sub"
    
    if os.path.exists("service.json"):
        credentials = service_account.Credentials.from_service_account_file("service.json")
        subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
        if not project_id:
            project_id = credentials.project_id
    else:
        subscriber = pubsub_v1.SubscriberClient()

    if not project_id:
        print("Error: No Project ID found.")
        return

    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    
    print(f"Listening for messages on {subscription_path}...")
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()

if __name__ == "__main__":
    main()
