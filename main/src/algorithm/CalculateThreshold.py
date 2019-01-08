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

    def train(self, **data):
        """
        计算算法参数
        :param data: 算法所需的数据
        :return: 自适应阈值
        """

        def method_1(data_list, rate):
            if not isinstance(data_list, list) or not isinstance(rate, float):
                raise Exception("非法参数数据类型")
            if len(data_list) < 5:
                raise Exception("数据过少")
            if isinstance(data_list[0], float):
                raise Exception("列表元素数据类型非法")
            mean = sum(data_list) / len(data_list)
            stdvar = (sum(map(lambda x: (x - mean) ** 2, data_list)) / len(data_list)) ** 0.5
            return mean - rate * stdvar

        def method_2(data_list, rate):
            if not isinstance(data_list, list) or not isinstance(rate, float):
                raise Exception("非法参数数据类型")
            if len(data_list) < 5:
                raise Exception("数据过少")
            if isinstance(data_list[0], float):
                raise Exception("列表元素数据类型非法")
            return (sum(data_list) / len(data_list)) * rate

        def method_3(theoretical_value, rate):
            if not isinstance(theoretical_value, float) or not isinstance(rate, float):
                raise Exception("非法参数数据类型")
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
