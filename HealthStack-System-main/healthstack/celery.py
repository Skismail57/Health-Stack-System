"""
Celery Configuration for HealthStack
Handles asynchronous tasks like email sending, report generation, etc.
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthstack.settings')

app = Celery('healthstack')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery Beat Schedule for periodic tasks
app.conf.beat_schedule = {
    # Send appointment reminders every hour
    'send-appointment-reminders': {
        'task': 'hospital.tasks.send_appointment_reminders',
        'schedule': crontab(minute=0),  # Every hour
    },
    # Clean up expired sessions daily
    'cleanup-expired-sessions': {
        'task': 'hospital.tasks.cleanup_expired_sessions',
        'schedule': crontab(hour=3, minute=0),  # Daily at 3 AM
    },
    # Generate daily statistics
    'generate-daily-stats': {
        'task': 'hospital.tasks.generate_daily_statistics',
        'schedule': crontab(hour=23, minute=55),  # Daily at 11:55 PM
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task for testing Celery"""
    print(f'Request: {self.request!r}')
