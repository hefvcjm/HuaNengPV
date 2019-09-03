# coding=utf-8
import numpy as np
from . import check


def check_enable(powers: list or np.array):
    """
    检测当前是否在正常发电，以全站逆变器功率为依据，不发电状态为全站逆变器输出功率综合小于某个阈值，保存一个全站状态变量
    连续n次功率小于阈值说明当前为不发电状态
    :param powers: 电站全部逆变器输出功率
    :return: 当前判断状态，True发电, False不发电
    ----------------------------------------------------
    参数说明如上所述
    触发条件：查询触发
    """
    return check(powers)
