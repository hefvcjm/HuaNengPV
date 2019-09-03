# coding=utf-8
# 电站状态，是否当前在发电，根据数据实时更新
import numpy as np

COUNT_THRESHOLD = 2
STAT_COUNT = 0
STATION_ENABLE = False


def check(powers):
    global COUNT_THRESHOLD, STAT_COUNT, STATION_ENABLE
    threshold = 10
    temp = np.array(powers).sum() > threshold
    if temp:
        STAT_COUNT += 1
    else:
        STAT_COUNT = 0
        STATION_ENABLE = False
    if STAT_COUNT > COUNT_THRESHOLD:
        STATION_ENABLE = True
        STAT_COUNT = COUNT_THRESHOLD
    return STATION_ENABLE


def wraps(assign_name):
    def update_name(func):
        def change(*args, **kwargs):
            temp = func(*args, **kwargs)
            setattr(temp, "__name__", assign_name)
            return temp

        return change

    return update_name


def check_station(default_func):
    """
    :param default_func: 不发电是返回构建的默认结果的构建函数
    :return:
    """

    def myfunc(func):
        @wraps(func.__name__)
        def wrap(*args, **kwargs):
            if STATION_ENABLE:
                return func
            else:
                return default_func

        return wrap()

    return myfunc
