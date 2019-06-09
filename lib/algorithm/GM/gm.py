# coding = utf-8
"""
灰色理论GM(1, 1)
"""

import numpy as np
import math


class gm:
    """
    等间距灰色预测
    """

    def __init__(self, data: list):
        """
        构造函数
        :param data: 等间隔数据列表
        """
        self.__data = np.array(data)
        self.__coef = None
        self.__calc_coef()

    def __calc_coef(self):
        """
        计算模型参数
        :return:
        """
        cum_sum = np.cumsum(self.__data)
        B = np.array([[-0.5 * (cum_sum[i] + cum_sum[i + 1]), 1] for i in range(cum_sum.size - 1)])
        Y = self.__data[1:].T
        self.__coef = np.linalg.inv(B.T @ B) @ B.T @ Y

    def predict_k(self, k):
        """
        预测第k点
        :param k:
        :return:
        """
        return (1 - math.e ** self.__coef[0]) * (self.__data[0] - self.__coef[1] / self.__coef[0]) * math.e ** (
                -self.__coef[0] * k)

    def predict_all(self, n):
        """
        预测前n项
        :param n:
        :return:
        """
        return np.array([self.predict_k(i) for i in range(1, n + 1)])

    def iter_predict_future(self, n):
        """
        迭代预测后n项
        :param n:
        :return:
        """
        result = list(self.__data)
        for i in range(n):
            _gm = gm(result)
            result.append(_gm.predict_k(len(result) + 1))
        return result


if __name__ == '__main__':
    data = [10, 8, 4, 9, 2, 4, 6, 4, 8, 2, 6, 7]
    model = gm(data)
    import matplotlib.pyplot as plt

    predict = model.predict_all(15)
    plt.plot(range(len(data)), data, predict)
    plt.show()
