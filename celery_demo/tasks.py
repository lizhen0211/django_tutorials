from time import sleep

from .celery import app


@app.task
def taska(x, y):
    print('===add begin===')
    sleep(5)
    print('===add end===')
    return x + y


@app.task
def taskb(x, y):
    return x * y
