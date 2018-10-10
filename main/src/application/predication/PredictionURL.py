# coding=utf-8
# 常规预测
from main.src.algorithm.Fitting import *


def pv_cell(history, highest_rate):
    """
    未发生故障时，正常情况下的刚光伏电池板寿命预测
    以光电转换率为预测指标
    :param history: 历史光电转换率列表
    :param highest_rate: 投产时的光电转换率
    :return: 一次多项式拟合结果参数和剩余寿命(a,b,err,rul)
    """
    if not isinstance(history, list):
        raise Exception("数据类型错误", history)
    if not (isinstance(highest_rate, int) or isinstance(highest_rate, float)):
        raise Exception("数据类型错误", highest_rate)
    if len(history) < 36:
        raise Exception("历史数据过少", len(history))
    if highest_rate < 15 or highest_rate > 50:
        raise Exception("投产时的光电转换率不合理(15,50)", highest_rate)
    fit, err = polyfit(range(len(history)), history, 1)
    a = fit[0]
    b = fit[1]
    rul = -(history[-1] - highest_rate * 0.8) / a
    return a, b, err, rul
