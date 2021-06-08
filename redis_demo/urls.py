from django.conf.urls import url

from cookie_demo.views import SetCookieView, DeleteCookieView
from redis_demo.views import SetRedisCacheView, GetRedisCacheView

urlpatterns = [
    url(r'^redis/set_cache$', SetRedisCacheView.as_view()),
    url(r'^redis/get_cache$', GetRedisCacheView.as_view()),
]
