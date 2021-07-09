from time import sleep

from .celery import app


@app.task
def add(x, y):
    print('===add begin===')
    sleep(5)
    print('===add end===')
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)
