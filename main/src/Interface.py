from main.src.algorithm.BaseAlgorithm import BaseAlgorithm


class Formatter:
    """
    数据格式化formatter
    """

    def on_format(self, formatted_data):
        pass


class InputFormatter(Formatter):
    """
    输入数据格式化formatter
    """

    def on_format(self, formatted_data):
        super(InputFormatter, self).on_format(formatted_data)


class ResultFormatter(Formatter):
    """
    输出结果格式化formatter
    """

    def on_format(self, formatted_data):
        super(ResultFormatter, self).on_format(formatted_data)


class PreDataHandler:
    """
    输入数据预处理handler
    """

    def handle(self, handled_data):
        pass


class ResultReviser:
    """
    输出结果修正reviser
    """

    def revise(self, revised_data):
        pass


class OnExecuteListener:
    """
    执行监听器listener
    """

    def __init__(self):
        pass

    def on_success(self, result):
        pass

    def on_failure(self, error):
        pass
