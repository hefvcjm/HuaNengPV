# 回归算法
import numpy as np
from .BaseAlgorithm import BaseAlgorithm


class Polyfit(BaseAlgorithm):
    __x = None
    __y = None
    __deg = None

    def __init__(self, x, y, deg):
        """
        构造方法
        :param x: x
        :param y: y
        :param deg: 拟合多项式的次数
        """
        super().__init__()
        self.__x = x
        self.__y = y
        self.__deg = deg

    def __polyfit(self):
        """
        多项式拟合
        :return: （拟合系数，误差）
        """
        fit = np.polyfit(self.__x, self.__y, self.__deg)
        res = np.std(np.array([np.polyval(fit, i) for i in self.__x]) - np.array(self.__y))
        return fit, res

    def run(self):
        if super()._on_execute_listener is None:
            raise TypeError("on_execute_listener不能为None，请使用set_execute_listener方法设置")
        fit, res = self.__polyfit()
        super()._on_execute_listener.on_success(fit, res)
