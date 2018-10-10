from main.src.Interface import *


class BaseAlgorithm:
    """
    算法基类，所有算法实现都需要继承该类
    """
    # 执行结果回调接口
    _on_execute_listener = None

    def __init__(self):
        pass

    def set_execute_listener(self, on_execute_listener: OnExecuteListener):
        """
        设置算法执行结果回调结果
        :param on_execute_listener: OnExecuteListener接口
        """
        self._on_execute_listener = on_execute_listener

    def run(self):
        """
        执行算法
        """
        pass
