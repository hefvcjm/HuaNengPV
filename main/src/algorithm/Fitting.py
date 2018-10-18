# 回归算法
import numpy as np


class Polyfit:
    __x = None
    __y = None
    __deg = None

    def __init__(self, x, y, deg):
        self.__x = x
        self.__y = y
        self.__deg = deg

    def polyfit(self):
        """
        多项式拟合
        :return: （拟合系数，误差）
        """
        fit = np.polyfit(self.__x, self.__y, self.__deg)
        res = np.std(np.array([np.polyval(fit, i) for i in self.__x]) - np.array(self.__y))
        return fit, res
