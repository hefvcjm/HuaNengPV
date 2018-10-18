from main.src.framework.Interface import *
from . import BaseAlgorithm


class Execute:
    """
    定义算法模块执行流程
    """

    def __init__(self):
        pass

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

    def set_data(self, data):
        self.__input = data

    def get_data(self):
        return self.__input

    def set_execute_listener(self, execute_listener: OnExecuteListener):
        if execute_listener is not None:
            self.__on_execute_listener = execute_listener

    def get_execute_listener(self):
        return self.__on_execute_listener

    def set_formatter(self, input_formatter: Formatter, result_formatter: Formatter):
        if input_formatter is not None:
            self.__input_formatter = input_formatter
        if result_formatter is not None:
            self.__result_formatter = result_formatter

    def get_input_formatter(self):
        return self.__input_formatter

    def get_result_formatter(self):
        return self.__result_formatter

    def set_pre_data_handler(self, handler: Handler):
        if handler is not None:
            self.__pre_data_handler = handler

    def get_pre_data_handler(self):
        return self.__pre_data_handler

    def set_reviser(self, reviser: Reviser):
        if reviser is not None:
            self.__result_reviser = reviser

    def get_reviser(self):
        return self.__result_reviser

    def set_algorithm(self, algorithm: BaseAlgorithm):
        self.__algorithm = algorithm

    def get_algorithm(self):
        return self.__algorithm

    def execute(self):
        if self.__algorithm is None:
            raise TypeError("executor不能为None，可以调用set_algorithm_executor进行设置")
        self.set_formatter(self.__input_formatter if self.__input_formatter is not None else self.__InputFormatter()
                           ,
                           self.__result_formatter if self.__result_formatter is not None else self.__ResultFormatter())
        # 设置数据预处理handler
        self.set_pre_data_handler(
            self.__pre_data_handler if self.__pre_data_handler is not None else self.__PreDataHandler())
        # 设置结果修正reviser
        self.set_reviser(self.__result_reviser if self.__result_reviser is not None else self.__ResultReviser())
        # 设置执行需要执行的算法
        formatted_input = self.__input_formatter.format(self.__input)
        pre_handled_input = self.__pre_data_handler.handle(formatted_input)
        self.__algorithm.set_data(pre_handled_input)
        self.__algorithm.set_execute_listener(self.__AlgorithmListener(self))
        self.__algorithm.run()

    class __AlgorithmListener(OnExecuteListener):
        """
        默认算法执行结束回调接口
        """
        __outer = None

        def __init__(self, outer):
            self.__outer = outer

        def on_success(self, result):
            revised = self.__outer.get_reviser().revise(result)
            formatted = self.__outer.get_result_formatter().format(revised)
            self.__outer.get_execute_listener().on_success(formatted)

        def on_failure(self, error):
            self.__outer.get_execute_listener().on_failure(error)

    class __InputFormatter(Formatter):
        """
        默认输入数据格式化formatter
        """

        def format(self, data):
            return data

    class __ResultFormatter(Formatter):
        """
        默认输出结果格式化formatter
        """

        def format(self, data):
            return data

    class __PreDataHandler(Handler):
        """
        默认输入数据预处理handler
        """

        def handle(self, data):
            return data

    class __ResultReviser(Reviser):
        """
        默认输出结果修正reviser
        """

        def revise(self, data):
            return data
