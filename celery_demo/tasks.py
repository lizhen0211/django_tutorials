from time import sleep

from .celery import app


@app.task
def taska(x, y):
    print('===taska add begin===')
    sleep(5)
    print('===taska add end===')
    return x + y


@app.task
def taskb(x, y):
    print('===taskb mult begin===')
    return x * y
    print('===taskb mult end===')
