import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'enigma_recruitment_task.settings')

app = Celery('enigma_recruitment_task')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
