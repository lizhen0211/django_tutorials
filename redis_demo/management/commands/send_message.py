import json
import random

import requests
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for _ in range(0, 10):
            data_item = {'id': random.choice(range(5)), 'val': random.choice('abcdefghijklmnopqrstuvwxyz')}
            print(data_item)
            requests.post('http://192.168.6.49:8010/redis/native_set_cache_group_by_key', data=json.dumps(data_item))
        self.stdout.write(self.style.SUCCESS('ok'))
