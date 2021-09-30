from redis.sentinel import Sentinel

sentinel = None
_cached_master_client = None
_cached_slave_client = None

# Redis缓存
REDIS_SENTINEL = [
    ('127.0.0.1', 26379),
    ('127.0.0.1', 26379)
]


def get_redis_conn(readonly=False):
    """
    连接redis数据库
    :param readonly:
    :return:
    """
    global sentinel, _cached_master_client, _cached_slave_client
    if not sentinel:
        sentinel = Sentinel(REDIS_SENTINEL, socket_timeout=0.1)
    if not _cached_master_client:
        _cached_master_client = sentinel.master_for('host6379')
    if not _cached_slave_client:
        _cached_slave_client = sentinel.slave_for('host6379')
    return _cached_slave_client if readonly else _cached_master_client
