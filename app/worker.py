from celery import Celery, Task
from services.email_handler import fetch_and_reply
import os
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("tasks", broker=REDIS_URL)

class EmailTaskWithRetry(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 5, 'countdown': 60}
    retry_backoff = True

@celery_app.task(bind=True, base=EmailTaskWithRetry)
def run_email_agent_task(self, customer: dict):
    fetch_and_reply(customer)

