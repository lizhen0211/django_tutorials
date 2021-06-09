# Create your views here.
from django.core.cache import caches
from django.views.generic.base import View
from django_redis import get_redis_connection

from utils.responses import HttpJsonResponse

# django redis cache
redis_cache = caches['default']
# 原生redis cache
redis_connection = get_redis_connection("default")


# https://django-redis-chs.readthedocs.io/zh_CN/latest/ #Django redis教程
# https://www.runoob.com/w3cnote/python-redis-intro.html #Python redis教程
class SetDjangoRedisCacheView(View):
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
        redis_cache.set("visit:12306:totals", 34634)
        print(redis_cache.get("visit:12306:totals"))
        redis_cache.incr("visit:12306:totals")
        print(redis_cache.get("visit:12306:totals"))

        return HttpJsonResponse(status=200)


class GetDjangoRedisCacheView(View):
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


class SetCacheView(View):
    def post(self, request):
        redis_connection.set('name', 'runoob')  # 设置 name 对应的值
        print(redis_connection['name'])  # 取出键 name 对应的值
        print(redis_connection.get('name'))  # 取出键 name 对应的值
        print(type(redis_connection.get('name')))  # 查看类型
        # 解码 将byte转成string
        decode = redis_connection.get('name').decode('UTF-8', 'strict')
        print(decode)
        print(type(decode))
        return HttpJsonResponse(status=200)


class SetCacheParamView(View):
    def post(self, request):
        # 1.ex - 过期时间（秒） 这里过期时间是3秒，3秒后p，键food的值就变成None
        redis_connection.set('food', 'mutton', ex=3)  # key是"food" value是"mutton" 将键值对存入redis缓存
        print(redis_connection.get('food'))  # mutton 取出键food对应的值
        # 2.px - 过期时间（豪秒） 这里过期时间是3豪秒，3毫秒后，键foo的值就变成None
        redis_connection.set('food', 'beef', px=3)
        print(redis_connection.get('food'))
        # 3.nx - 如果设置为True，则只有name不存在时，当前set操作才执行 （新建）
        print(redis_connection.set('fruit', 'watermelon', nx=True))  # True--不存在
        # 如果键fruit不存在，那么输出是True；如果键fruit已经存在，输出是None

        # 4.xx - 如果设置为True，则只有name存在时，当前set操作才执行 （修改）
        print((redis_connection.set('fruit', 'watermelon', xx=True)))  # True--已经存在
        # 如果键fruit已经存在，那么输出是True；如果键fruit不存在，输出是None

        # 5.setnx(name, value) 设置值，只有name不存在时，执行设置操作（添加）
        print(redis_connection.setnx('fruit1', 'banana'))  # fruit1不存在，输出为True

        # 6.setex(name, time, value) time - 过期时间（数字秒 或 timedelta对象）
        redis_connection.setex("fruit2", 5, "orange")
        print(redis_connection.get('fruit2'))
        # time.sleep(5)
        print(redis_connection.get('fruit2'))  # 5秒后，取值就从orange变成None

        # 8.mset(*args, **kwargs) 批量设置值
        redis_connection.mget({'k1': 'v1', 'k2': 'v2'})
        redis_connection.mset({'k1': 'v1', 'k2': 'v2'})  # 这里k1 和k2 不能带引号 一次设置多个键值对
        print(redis_connection.mget("k1", "k2"))  # 一次取出多个键对应的值
        print(redis_connection.mget("k1"))

        # 9.mget(keys, *args) 批量获取
        print(redis_connection.mget('k1', 'k2'))
        print(redis_connection.mget(['k1', 'k2']))
        print(redis_connection.mget("fruit", "fruit1", "fruit2", "k1", "k2"))  # 将目前redis缓存中的键对应的值批量取出来

        return HttpJsonResponse(status=200)


class SetCacheListView(View):
    def post(self, request):
        redis_connection.lpush("list1", 11, 22, 33)
        print(redis_connection.lrange('list1', 0, -1))

        redis_connection.rpush("list2", 11, 22, 33)  # 表示从右向左操作
        print(redis_connection.llen("list2"))  # 列表长度
        print(redis_connection.lrange("list2", 0, 3))  # 切片取出值，范围是索引号0-3

        return HttpJsonResponse(status=200)


class SetCacheSetView(View):
    def post(self, request):
        redis_connection.sadd("set1", 33, 44, 55, 66)  # 往集合中添加元素
        print(redis_connection.scard("set1"))  # 集合的长度是4
        print(redis_connection.smembers("set1"))  # 获取集合中所有的成员
        return HttpJsonResponse(status=200)
