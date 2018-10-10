# coding=utf-8
"""
诊断简单故障的程序
"""


def simple_compare(value, threshold, direction):
    """
    简单阈值比较
    :param value: 需要比较的值
    :param threshold: 阈值
    :param direction: 上限或者下限
    :return: 比较结果
    """
    if not (isinstance(value, int) or isinstance(value, float)):
        raise Exception("数据类型错误", value)
    if not (isinstance(threshold, int) or isinstance(threshold, float)):
        raise Exception("数据类型错误", threshold)
    if direction == "up":
        if value > threshold:
            return True
        return False
    elif direction == "down":
        if value < threshold:
            return True
        return False
    else:
        raise Exception("比较方向字段错误", direction)


def simple_compare_up(value, threshold):
    """
    上限阈值比较
    :param value: 需要比较的值
    :param threshold: 上限阈值
    :return: 比较结果
    """
    return simple_compare(value, threshold, "up")


def simple_compare_down(value, threshold):
    """
    下限阈值比较
    :param value: 需要比较的值
    :param threshold: 上限阈值
    :return: 比较结果
    """
    return simple_compare(value, threshold, "down")
