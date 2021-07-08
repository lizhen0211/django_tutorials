# Set the default Django settings module for the 'celery' program.
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_tutorials.settings')

# app = Celery('django_tutorials')
app = Celery('django_tutorials', broker='amqp://rabbit:123456@localhost:5672//django_tutorials', backend='rpc://', include=['celery_demo.tasks'])
# app = Celery('django_tutorials', broker='amqp://', backend='rpc://')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()
