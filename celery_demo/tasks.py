import json
from time import sleep

import requests
from django_redis import get_redis_connection

from .celery import app

redis_connection = get_redis_connection("default")


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


@app.task
def forwardtask(json_str):
    json_data = json.loads(json_str)
    for _ in redis_connection.lrange(json_data['id'], 0, -1):
        print('before forward:' + str(redis_connection.lrange(json_data['id'], 0, -1)), end=" ")
        # print(str(redis_connection.lrange(json_data['id'], 0, -1)))
        pop_item = redis_connection.rpop(json_data['id'])
        requests.post('http://192.168.6.49:8010/redis/native_set_cache_forward',
                      data=json.dumps({json_data['id']: pop_item.decode("utf-8")}))
        # print('pop ' + str(json_data['id']) + ":" + str(pop_item))
        # print('after forward:' + str(json_data['id']), redis_connection.lrange(json_data['id'], 0, -1))
