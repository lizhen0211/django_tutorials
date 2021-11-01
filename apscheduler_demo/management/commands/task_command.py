import time

from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        struct_time = time.localtime()
        print(struct_time)
        self.stdout.write(self.style.SUCCESS('task command exec finish'))
