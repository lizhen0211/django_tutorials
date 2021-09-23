import datetime
import json
import random

import requests
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for _ in range(0, 50):
            now = datetime.datetime.now().strftime("%H:%M:%S.%f")
            id_val = random.choice(range(2))
            # random.choice('abcdefghijklmnopqrstuvwxyz')
            data_item = {'id': id_val, 'val': '%s:%s' % (id_val, now)}
            print(data_item)
            requests.post('http://192.168.6.49:8010/redis/native_set_cache_group_by_key', data=json.dumps(data_item))
        self.stdout.write(self.style.SUCCESS('ok'))
