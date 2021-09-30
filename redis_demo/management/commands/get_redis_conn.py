from django.core.management import BaseCommand

from redis_demo.redis_client import get_redis_conn


class Command(BaseCommand):
    def handle(self, *args, **options):
        print(get_redis_conn())
        self.stdout.write(self.style.SUCCESS('ok'))
