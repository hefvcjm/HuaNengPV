from main.src.Interface import *


class Execute:
    """
    定义算法模块执行流程
    """
    # 执行listener接口，需要实现其中的on_success和on_failure方法
    __on_execute_listener = None
    # 输入原始数据
    __input = None
    # 格式化输入接口
    __input_formatter = None
    # 数据预处理接口
    __pre_data_handler = None
    # 结果修正接口
    __result_reviser = None
    # 格式化结果输出接口
    __result_formatter = None
    # 算法执行器
    __algorithm = None

    def get_data(self):
        pass

    def set_formatter(self, input_formatter: Formatter, result_formatter: Formatter):
        self.__input_formatter = input_formatter
        self.__result_formatter = result_formatter

    def set_pre_data_handler(self, handler: PreDataHandler):
        self.__pre_data_handler = handler

    def set_reviser(self, reviser: ResultReviser):
        self.__result_reviser = reviser

    def set_algorithm(self, algorithm: BaseAlgorithm):
        self.__algorithm = algorithm

    def execute(self):
        if self.__algorithm is None:
            raise TypeError("executor不能为None，可以调用set_algorithm_executor进行设置")
        self.__algorithm.run()
