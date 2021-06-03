from django.conf.urls import url

from cookie_demo.views import SetCookieView, DeleteCookieView

urlpatterns = [
    url(r'^cookie/set_cookie$', SetCookieView.as_view()),
    url(r'^cookie/del_cookie$', DeleteCookieView.as_view()),

]
