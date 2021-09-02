from django.conf.urls import url

from db_demo.views import DBConnectionReleaseView

urlpatterns = [
    url(r'^db/db_connection_release$', DBConnectionReleaseView.as_view()),

]
