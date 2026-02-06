import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_django_project.settings')

app = Celery('simple_django_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# namespace='CELERY' means all celery-related config keys should
# have a `CELERY_` prefix (e.g., CELERY_BROKER_URL).
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Schedule periodic tasks
app.conf.beat_schedule = {
    'sync-plaid-transactions-daily': {
        'task': 'transactions.tasks.sync_plaid_transactions_for_all_users',
        # 'schedule': crontab(hour=2, minute=0),  # Run daily at 2 AM
        'schedule': 30.0,  # Run every 30 seconds
        # Alternative: 'schedule': 3600.0,  # Run every hour (in seconds)
    },
}