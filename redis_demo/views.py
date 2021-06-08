from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from django.core.cache import caches

from utils.responses import HttpJsonResponse

redis_cache = caches['default']


class SetRedisCacheView(View):
    def post(self, request):
        print(redis_cache)
        redis_cache.set('key1', 'val1', timeout=None)
        return HttpJsonResponse(status=200)


class GetRedisCacheView(View):
    def get(self, request):
        obj = {'key1': redis_cache.get('key1')}
        return HttpJsonResponse(obj, status=200)
