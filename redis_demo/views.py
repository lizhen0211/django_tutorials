# Create your views here.
from django.core.cache import caches
from django.views.generic.base import View
from django_redis import get_redis_connection

from utils.responses import HttpJsonResponse

# django redis cache
redis_cache = caches['default']
# 原生redis cache
redis_connection = get_redis_connection("default")


# redis 介绍
# https://segmentfault.com/a/1190000008645186

# Django redis教程
# https://django-redis-chs.readthedocs.io/zh_CN/latest/#

# Python redis教程
# https://www.runoob.com/w3cnote/python-redis-intro.html
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
        print(redis_cache.set('foo_3', '3'))
        print(redis_cache.set('foo_4', '4'))
        print(redis_cache.set('foo_5', '5'))

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

        # 10.getset(name, value) 设置新值并获取原来的值
        print(redis_connection.getset("food", "barbecue"))  # 设置的新值是barbecue 设置前的值是beef

        # 18.incr(self, name, amount=1)
        # 自增 name 对应的值，当 name 不存在时，则创建 name＝amount，否则，则自增。
        redis_connection.set("foo", 123)
        print(redis_connection.mget("foo", "foo1", "foo2", "k1", "k2"))
        redis_connection.incr("foo", amount=1)
        print(redis_connection.mget("foo", "foo1", "foo2", "k1", "k2"))

        # 19.incrbyfloat(self, name, amount=1.0)
        # 自增 name对应的值，当name不存在时，则创建name＝amount，否则，则自增。
        redis_connection.set("foo1", "123.0")
        redis_connection.set("foo2", "221.0")
        print(redis_connection.mget("foo1", "foo2"))
        redis_connection.incrbyfloat("foo1", amount=2.0)
        redis_connection.incrbyfloat("foo2", amount=3.0)
        print(redis_connection.mget("foo1", "foo2"))

        # 20.decr(self, name, amount=1)
        # 自减 name 对应的值，当 name 不存在时，则创建 name＝amount，否则，则自减。
        redis_connection.decr("foo4", amount=3)  # 递减3
        redis_connection.decr("foo1", amount=1)  # 递减1
        print(redis_connection.mget("foo1", "foo4"))

        # 21.append(key, value)z
        # 在redis name对应的值后面追加内容
        print(redis_connection.mget("name"))
        redis_connection.append("name", "haha")  # 在name对应的值junxi后面追加字符串haha
        print(redis_connection.mget("name"))

        # 清空当前库中的所有 key
        # redis_connection.flushdb()
        # 清空整个 Redis 服务器的数据
        # redis_connection.flushall()
        return HttpJsonResponse(status=200)


class HashView(View):
    def post(self, request):
        # redis 基本命令 hash
        # 1、单个增加--修改(单个取出)--没有就新增，有的话就修改
        # hset(name, key, value)
        # 注：hsetnx(name, key, value) 当name对应的hash中不存在当前key时则创建（相当于添加）
        redis_connection.hset("hash1", "k1", "v1")
        redis_connection.hset("hash1", "k2", "v2")
        print(redis_connection.hkeys("hash1"))  # 取hash中所有的key
        print(redis_connection.hget("hash1", "k1"))  # 单个
        print(redis_connection.hmget("hash1", "k1", "k2"))  # 多个取hash的key对应的值# 取hash的key对应的值
        print(redis_connection.hget("hash1", "k2"))

        # 2、批量增加（取出）
        # hmset(name, mapping)
        # 在name对应的hash中批量设置键值对
        # 参数：
        #   name - redis的name
        #   mapping - 字典，如：{'k1':'v1', 'k2': 'v2'}
        redis_connection.hmset("hash2", {"k2": "v2", "k3": "v3"})
        print(redis_connection.hget("hash2", "k2"))  # 单个取出"hash2"的key-k2对应的value
        print(redis_connection.hmget("hash2", "k2", "k3"))  # 批量取出"hash2"的key-k2 k3对应的value --方式1
        print(redis_connection.hmget("hash2", ["k2", "k3"]))  # 批量取出"hash2"的key-k2 k3对应的value --方式2

        # 3、取出所有的键值对
        print(redis_connection.hgetall("hash1"))

        # 4、得到所有键值对的格式 hash长度
        print(redis_connection.hlen("hash1"))

        # 5、得到所有的keys（类似字典的取所有keys）
        # 获取name对应的hash中所有的key的值
        print(redis_connection.hkeys("hash1"))

        # 6、得到所有的value（类似字典的取所有value）
        # 获取name对应的hash中所有的value的值
        print(redis_connection.hvals("hash1"))

        # 7、判断成员是否存在（类似字典的in）
        # hexists(name, key)
        print(redis_connection.hexists("hash1", "k4"))  # False 不存在
        print(redis_connection.hexists("hash1", "k1"))  # True 存在

        # 8、删除键值对
        # hdel(name,*keys)
        # 将name对应的hash中指定key的键值对删除
        print(redis_connection.hgetall("hash1"))
        redis_connection.hset("hash1", "k2", "v222")  # 修改已有的key k2
        redis_connection.hset("hash1", "k11", "v1")  # 新增键值对 k11
        redis_connection.hdel("hash1", "k1")  # 删除一个键值对
        print(redis_connection.hgetall("hash1"))

        # 9、自增自减整数(将key对应的value--整数 自增1或者2，或者别的整数 负数就是自减)
        # hincrby(name, key, amount=1)
        redis_connection.hset("hash1", "k3", 123)
        redis_connection.hincrby("hash1", "k3", amount=-1)
        print(redis_connection.hgetall("hash1"))
        redis_connection.hincrby("hash1", "k4", amount=1)  # 不存在的话，value默认就是1
        print(redis_connection.hgetall("hash1"))

        # 10、自增自减浮点数(将key对应的value--浮点数 自增1.0或者2.0，或者别的浮点数 负数就是自减)
        # hincrbyfloat(name, key, amount=1.0)

        return HttpJsonResponse(status=200)


class SetCacheListView(View):
    def post(self, request):
        # redis基本命令 list
        # 1.增加（类似于list的append，只是这里是从左边新增加）--没有就新建
        # lpush(name,values)
        redis_connection.lpush("list1", 11, 22, 33)
        print(redis_connection.lrange('list1', 0, -1))
        # 保存顺序为: 33, 22, 11

        redis_connection.rpush("list2", 11, 22, 33)  # 表示从右向左操作
        print(redis_connection.llen("list2"))  # 列表长度
        print(redis_connection.lrange("list2", 0, 3))  # 切片取出值，范围是索引号0-3

        # 2.增加（从右边增加）--没有就新建
        redis_connection.rpush("list2", 44, 55, 66)  # 在列表的右边，依次添加44,55,66
        print(redis_connection.llen("list2"))  # 列表长度
        print(redis_connection.lrange("list2", 0, -1))  # 切片取出值，范围是索引号0到-1(最后一个元素)

        # 3.往已经有的name的列表的左边添加元素，没有的话无法创建
        # 在name对应的list中添加元素，只有name已经存在时，值添加到列表的最左边
        redis_connection.lpushx("list10", 10)  # 这里list10不存在
        print(redis_connection.llen("list10"))  # 0
        print(redis_connection.lrange("list10", 0, -1))  # []
        redis_connection.lpushx("list2", 77)  # 这里"list2"之前已经存在，往列表最左边添加一个元素，一次只能添加一个
        print(redis_connection.llen("list2"))  # 列表长度
        print(redis_connection.lrange("list2", 0, -1))  # 切片取出值，范围是索引号0到-1(最后一个元素

        # 4.往已经有的name的列表的右边添加元素，没有的话无法创建
        redis_connection.rpushx("list2", 99)  # 这里"foo_list1"之前已经存在，往列表最右边添加一个元素，一次只能添加一个
        print(redis_connection.llen("list2"))  # 列表长度
        print(redis_connection.lrange("list2", 0, -1))  # 切片取出值，范围是索引号0到-1(最后一个元素)

        # 5.新增（固定索引号位置插入元素）
        # 6.修改（指定索引号进行修改）
        # 7.删除（指定值进行删除）
        # 8.删除并返回
        # 9.删除索引之外的值
        # 10.取值（根据索引号取值）
        # 11.移动 元素从一个列表移动到另外一个列表
        # 12.移动 元素从一个列表移动到另外一个列表 可以设置超时
        # 13.一次移除多个列表
        # 14.自定义增量迭代
        return HttpJsonResponse(status=200)


class SetCacheSetView(View):
    def post(self, request):
        # 6、redis基本命令 set

        # 1.新增 sadd(name,values)
        # name - 对应的集合中添加元素
        redis_connection.sadd("set1", 33, 44, 55, 66)  # 往集合中添加元素

        # 2.获取元素个数 类似于len
        print(redis_connection.scard("set1"))

        # 3.获取集合中所有的成员
        print(redis_connection.smembers("set1"))
        # 获取集合中所有的成员--元组形式
        # sscan(name, cursor=0, match=None, count=None)
        print(redis_connection.sscan("set1"))
        # 获取集合中所有的成员--迭代器的方式
        # sscan_iter(name, match=None, count=None)
        # 同字符串的操作，用于增量迭代分批获取元素，避免内存消耗太大
        for i in redis_connection.sscan_iter("set1"):
            print(i)

        # 4.差集
        # 6.交集
        return HttpJsonResponse(status=200)
