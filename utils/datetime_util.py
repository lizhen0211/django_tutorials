import datetime
import time

from django.utils import timezone

local_tz = timezone.get_current_timezone()


def get_cur_timestamp():
    """
        获取当前时间戳
    """
    return time.time()


def timestamp_to_datetime(timestamp, tz=None):
    """
        timestamp转datetime
    :param timestamp:
    :param tz:
    :return:
    """
    tz = tz if tz else local_tz
    return datetime.datetime.fromtimestamp(timestamp, tz=tz)


def timestamp_to_yyyy_mm_dd_hh_mm_ss(timestamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))


if __name__ == '__main__':
    import django

    django.setup()
    print(get_cur_timestamp())
    print(timestamp_to_datetime(time.time()))
    print(timestamp_to_yyyy_mm_dd_hh_mm_ss(time.time() - 24 * 60 * 60))
