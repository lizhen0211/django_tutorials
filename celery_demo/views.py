import time

from django.http import HttpResponse
from django.shortcuts import render

# https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html

# Create your views here.
from django.views.generic.base import View
from celery_demo.tasks import taska, taskb


class SimpleTaskView(View):
    def get(self, request):
        resulta = taska.delay(4, 4)
        readya = resulta.ready()
        print(readya)

        resultb = taskb.delay(4, 4)
        readyb = resultb.ready()
        print(readyb)

        return HttpResponse()
