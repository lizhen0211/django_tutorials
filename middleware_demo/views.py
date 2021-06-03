# Create your views here.
from django.views.generic.base import View


class ASimpleMiddlewareView(View):
    def get(self, request):
        print('')
