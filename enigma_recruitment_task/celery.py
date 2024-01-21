import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'enigma_recruitment_task.settings')

app = Celery('enigma_recruitment_task')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'every 24h': {
        "task": "send_payment_reminder_email",
        'schedule': 86400.0,
    }
}

app.autodiscover_tasks()
