from main.src.framework.Execute import *
from main.src.application.predication.PredictionURL import *
import matplotlib.pyplot as plt
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']


class InputFormatter(Formatter):
    """
    默认输入数据格式化formatter
    """

    def format(self, data):
        return data


class ResultFormatter(Formatter):
    """
    默认输出结果格式化formatter
    """

    def format(self, data):
        return data


class PreDataHandler(Handler):
    """
    默认输入数据预处理handler
    """

    def handle(self, data):
        return data


class ResultReviser(Reviser):
    """
    默认输出结果修正reviser
    """

    def revise(self, data):
        return data


class ExecuteListener(OnExecuteListener):
    def on_success(self, result):
        pre = result[0] * range(300) + result[1]
        plt.plot(range(300), pre, c='g', label="预测曲线")
        plt.scatter(range(100), history, c='r', label='历史数据')
        plt.scatter(range(100, 300), x[100:], c='b', label='真实数据')
        plt.ylim((0, 20))
        plt.xlabel(u'投产月数', fontproperties="SimHei")
        plt.ylabel(u'光电转换率(%)', fontproperties="SimHei")
        plt.legend()
        plt.show()

    def on_failure(self, error):
        super().on_failure(error)


def rate(x):
    random = np.random.normal(0, 0.1, 1)[0]
    # print(random)
    return -0.012 * x + 18 + random


if __name__ == '__main__':
    x = [round(rate(x), 2) for x in range(300)]
    history = x[:100]
    execute = Execute()
    # 设置数据
    execute.set_data((history, 18))
    # 设置监听器
    execute.set_execute_listener(ExecuteListener())
    # 设置输入输出格式化formatter
    execute.set_formatter(InputFormatter(), ResultFormatter())
    # 设置数据预处理handler
    execute.set_pre_data_handler(PreDataHandler())
    # 设置结果修正reviser
    execute.set_reviser(ResultReviser())
    # 设置执行需要执行的算法
    execute.set_algorithm(PvCellUrlPrediction())
    # 执行
    execute.execute()
