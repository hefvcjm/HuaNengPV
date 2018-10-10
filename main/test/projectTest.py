# coding=utf-8
# test src code
from main.src.log.log import Log
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
from main.src.application.predication.PredictionURL import *
from main.src.calculate.General import *
import random

mpl.rcParams['font.sans-serif'] = ['SimHei']


def rate(x):
    random = np.random.normal(0, 0.1, 1)[0]
    # print(random)
    return -0.012 * x + 18 + random


if __name__ == '__main__':
    # Log.info("test")
    # x = [round(rate(x), 2) for x in range(300)]
    # print(x)
    # with open("data.txt", "w") as file:
    #     i = 0
    #     for item in x:
    #         file.write("%d\t%.2f\n" % (i, item))
    #         i = i + 1

    x = [round(rate(x), 2) for x in range(300)]
    history = x[:100]
    print(history)
    fit = pv_cell(history, 18)
    print(fit)
    pre = fit[0] * range(300) + fit[1]
    plt.plot(range(300), pre, c='g', label="预测曲线")
    plt.scatter(range(100), history, c='r', label='历史数据')
    plt.scatter(range(100, 300), x[100:], c='b', label='真实数据')
    plt.ylim((0, 20))
    plt.xlabel(u'投产月数', fontproperties="SimHei")
    plt.ylabel(u'光电转换率(%)', fontproperties="SimHei")
    plt.legend()
    plt.show()

    # data = []
    # for _ in range(100):
    #     data.append((random.uniform(0, 1), random.uniform(0, 1)))
    # print(inverter_efficiency(data))
