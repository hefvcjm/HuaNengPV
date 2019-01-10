# coding = utf-8
# 计算自适应阈值算法

class CalculateThreshold:
    """
    计算自适应阈值
    可选多种算法选择
    """

    def __init__(self, which):
        """
        构造方法
        :param which: 选择使用哪一种算法，字符串类型
        1:计算全局支路电流平均值（以某一节点单元为参考）和方差,设置固定偏差比率
        2:直接固定偏差比率
        3:理论值乘以固定偏差比率
        4:异常监测算法(暂未实现)
        """
        self.which = str(which)
        self.__predict_func = None
        self.__low_threshold = None
        self.__high_threshold = None

    def train(self, **data):
        """
        计算算法参数
        :param data: 算法所需的数据
        :return: 自适应阈值
        """

        def method_1(data_list, rate):
            if not isinstance(data_list, list) and (not isinstance(rate, float) or not isinstance(rate, int)):
                raise Exception("非法参数数据类型")
            if len(data_list) < 5:
                raise Exception("数据过少")
            if not isinstance(data_list[0], float) and not isinstance(data_list[0], int):
                raise Exception("列表元素数据类型非法")
            mean = sum(data_list) / len(data_list)
            std_var = (sum(map(lambda x: (x - mean) ** 2, data_list)) / len(data_list)) ** 0.5
            self.__low_threshold = mean - rate * std_var
            self.__predict_func = lambda x: x < self.__low_threshold
            return mean - rate * std_var

        def method_2(data_list, rate):
            if not isinstance(data_list, list) and not isinstance(rate, float):
                raise Exception("非法参数数据类型")
            if len(data_list) < 5:
                raise Exception("数据过少")
            if not isinstance(data_list[0], float) and not isinstance(data_list[0], int):
                raise Exception("列表元素数据类型非法")
            self.__low_threshold = (sum(data_list) / len(data_list)) * rate
            self.__predict_func = lambda x: x < self.__low_threshold
            return (sum(data_list) / len(data_list)) * rate

        def method_3(theoretical_value, rate):
            if not isinstance(theoretical_value, float) \
                    or not isinstance(rate, float) \
                    or not isinstance(rate, int) \
                    or not isinstance(theoretical_value, int):
                raise Exception("非法参数数据类型")
            self.__low_threshold = theoretical_value * rate
            self.__predict_func = lambda x: x < self.__low_threshold
            return theoretical_value * rate

        # def method_4(data_list):
        #     if not isinstance(data_list, list):
        #         raise Exception("非法参数数据类型")
        #     mean = sum(data_list) / len(data_list)
        #     var = sum(map(lambda x: (x - mean) ** 2, data_list)) / len(data_list)

        method = "method_" + str(self.which)
        method = eval(method)
        if method is None:
            raise Exception("无相应类型的算法", self.which)
        if callable(method):
            return method(**data)

    def predict(self, data):
        """
        利用上面以训练好的阈值参数进行预测
        :param data: 需要预测的数据，float或者float列表
        :return: 预测结果
        """
        if not isinstance(data, float) and not isinstance(data, int) and not isinstance(data, list):
            raise Exception("非法参数数据类型")
        if isinstance(data, list):
            if len(data) == 0 or (not isinstance(data[0], float) and not isinstance(data[0], int)):
                raise Exception("非法参数数据类型")
        if isinstance(data, float) or isinstance(data, int):
            return self.__predict_func(data)
        elif isinstance(data, list):
            return [self.__predict_func(item) for item in data]
        else:
            return None


instance = CalculateThreshold(1)
instance.train(data_list=[1, 2, 3, 2, 1, 5, 6, 3], rate=0.8)
print(instance.predict(0.2))
print(instance.predict([2, 4, 3]))
