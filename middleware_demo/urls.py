from django.conf.urls import url

from middleware_demo.views import ASimpleMiddlewareView

urlpatterns = [
    url(r'^middleware/a_simple_middleware$', ASimpleMiddlewareView.as_view())

]
