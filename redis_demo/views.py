from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from django.core.cache import caches

from utils.responses import HttpJsonResponse

redis_cache = caches['default']


# https://django-redis-chs.readthedocs.io/zh_CN/latest/

class SetRedisCacheView(View):
    def post(self, request):
        print(redis_cache)
        # 永不超时设置 timeout=None 永不超时
        redis_cache.set('foo_1', 'val1', timeout=None)
        # timeout=0 立即过期
        redis_cache.set('foo_2', 'val2', timeout=10)
        # 使用 persist
        redis_cache.persist("foo_1")
        redis_cache.ttl("foo_1")
        # 使用 expire
        redis_cache.expire("foo_2", timeout=20)
        redis_cache.ttl("foo_2")
        return HttpJsonResponse(status=200)


class GetRedisCacheView(View):
    def get(self, request):
        # 从key中取值
        print(redis_cache.get('foo_1'))
        print(redis_cache.get('foo_2'))
        # 获取缓存ttl
        print(redis_cache.ttl('foo_2'))
        # 使用通配符搜索的例子
        print(redis_cache.keys("foo_*"))
        # 使用迭代器取值
        print(next(redis_cache.iter_keys("foo_*")))
        return HttpJsonResponse('watch log from server', status=200)
