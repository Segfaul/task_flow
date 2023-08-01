import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('task_flow')
app.conf.broker_connection_retry_on_startup = False
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
