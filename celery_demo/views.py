from django.http import HttpResponse
# Create your views here.
from django.views.generic.base import View

from celery_demo.tasks import taska, taskb


# https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html


class SimpleTaskView(View):
    def get(self, request):
        resulta = taska.delay(4, 4)
        readya = resulta.ready()
        print(readya)

        resultb = taskb.delay(4, 4)
        readyb = resultb.ready()
        print(readyb)

        return HttpResponse()
