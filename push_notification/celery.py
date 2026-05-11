import os 
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'push_notification.settings')

app = Celery('push_notification')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()