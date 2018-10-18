# coding=utf-8
from main.src.algorithm.Fitting import *
from main.src.framework.BaseAlgorithm import *


class PvCellUrlPrediction(BaseAlgorithm):
    __history = None
    __highest_rate = None

    def __parse_data(self):
        print(self._data)
        self.__history = self._data[0]
        self.__highest_rate = self._data[1]

    def __init__(self):
        super().__init__()

    @staticmethod
    def prediction(history, highest_rate):
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
        fit, err = Polyfit(range(len(history)), history, 1).polyfit()
        a = fit[0]
        b = fit[1]
        rul = -(history[-1] - highest_rate * 0.8) / a
        return a, b, err, rul

    def run(self):
        self.__parse_data()
        if self._on_execute_listener is None:
            raise TypeError("on_execute_listener不能为None，请使用set_execute_listener方法设置")
        a, b, err, rul = self.prediction(self.__history, self.__highest_rate)
        self._on_execute_listener.on_success((a, b, err, rul))
