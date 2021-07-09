from django.conf.urls import url

from celery_demo.views import SimpleTaskView

urlpatterns = [
    url(r'^celery_demo/simple_task$', SimpleTaskView.as_view()),
]
