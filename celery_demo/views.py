import time

from django.http import HttpResponse
from django.shortcuts import render

# https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html

# Create your views here.
from django.views.generic.base import View
from celery_demo.tasks import taska


class SimpleTaskView(View):
    def get(self, request):
        result = taska.delay(4, 4)
        ready = result.ready()
        print(ready)
        return HttpResponse()
