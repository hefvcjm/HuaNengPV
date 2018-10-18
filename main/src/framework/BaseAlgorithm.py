class BaseAlgorithm:
    """
    算法基类，所有算法实现都需要继承该类
    """
    # 执行结果回调接口
    _on_execute_listener = None
    # 算法用到的数据
    _data = None

    def __init__(self):
        pass

    def set_data(self, data):
        self._data = data

    def set_execute_listener(self, on_execute_listener):
        """
        设置算法执行结果回调结果
        :param on_execute_listener: OnExecuteListener接口
        """
        self._on_execute_listener = on_execute_listener

    def get_execute_listener(self):
        return self._on_execute_listener

    def run(self):
        """
        执行算法
        """
        if self._on_execute_listener is None:
            raise TypeError("on_execute_listener不能为None，请使用set_execute_listener方法设置")
