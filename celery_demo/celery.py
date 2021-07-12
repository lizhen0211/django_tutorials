# Set the default Django settings module for the 'celery' program.
import os

from celery import Celery
from kombu import Queue, Exchange

from django_tutorials import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_tutorials.settings')

# app = Celery('django_tutorials')
app = Celery('django_tutorials', broker='amqp://rabbit:123456@localhost:5672//django_tutorials', backend='rpc://',
             include=['celery_demo.tasks'])
# app = Celery('django_tutorials', broker='amqp://', backend='rpc://')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

default_exchange = Exchange('default', type='direct')

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
    CELERY_TASK_RESULT_EXPIRES=settings.CELERY_TASK_RESULT_EXPIRES,
    CELERY_IGNORE_RESULT=settings.CELERY_IGNORE_RESULT,
    CELERYD_MAX_TASKS_PER_CHILD=settings.CELERYD_MAX_TASKS_PER_CHILD,
    CELERY_TASK_SERIALIZER=settings.CELERY_TASK_SERIALIZER,
    # CELERY_DEFAULT_QUEUE='receivedata_queue',

    CELERY_QUEUES=(
        Queue('biz_queue_a', default_exchange, routing_key='biz_queue_a_key',
              consumer_arguments={'x-priority': 20}),
        Queue('biz_queue_b', default_exchange, routing_key='biz_queue_b_key',
              consumer_arguments={'x-priority': 10}),
    ),

    CELERY_ROUTES={
        'celery_demo.tasks.taska': {'queue': 'biz_queue_a', 'routing_key': 'biz_queue_a_key'},
        'celery_demo.tasks.taskb': {'queue': 'biz_queue_b', 'routing_key': 'biz_queue_b_key'},
    },
)

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()
