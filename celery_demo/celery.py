from celery import Celery

app = Celery('celery_demo', broker='amqp://', backend='rpc://', include=['celery_demo.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
