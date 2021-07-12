from concurrent.futures.thread import ThreadPoolExecutor

from django.core.management import BaseCommand

import requests


class Command(BaseCommand):
    def handle(self, *args, **options):
        executor = ThreadPoolExecutor(max_workers=2)
        for _ in range(5):
            executor.submit(self.send_request_to_simple_task())
        self.stdout.write(self.style.SUCCESS('ok'))

    def send_request_to_simple_task(self):
        r = requests.get('http://192.168.6.49:8010/celery_demo/simple_task')
        print(r)
