from django.apps import AppConfig


class RedisDemoConfig(AppConfig):
    name = 'redis_demo'

    def ready(self):
        # python manage.py runserver --noreload 用此脚本执行保证ready函数中代码只执行一次，
        # python manage.py runserver ready函数中代码会执行两次
        print('redis_demo init in ready')
