# coding = utf-8
# 定义设备类基类


class BaseDevice:
    class _Input:
        def __init__(self, outer):
            """
            :param outer: 外部类
            """
            self.outer = outer

        def on_input(self, data):
            """
            有新的数据输入
            :param data: 输入数据，json格式，格式由上下文确定
            :return:
            """
            self.outer.run(data)

    class _Measurement:
        def __init__(self, outer):
            """
            :param outer: 外部类
            """
            self.outer = outer

        def on_measure(self, data):
            """
            生成测量量
            @:param data 测量数据
            :return: 由各个测量字段为键的字典
            """
            pass

    class _Output:
        def __init__(self):
            pass

        def on_output(self, data):
            """
            产生输出数据
            :param data: 输出数据，json格式，具体由上下文确定
            :return:
            """
            pass

    def __init__(self, config):
        """
        设备构造函数
        :param config: 设备配置
        """
        self.input = self._Input(self)
        self.output = self._Output()
        self.measurement = self._Measurement(self)
        self.data_in = None
        self.data_out = None
        self.data_measure = None
        self.data_config = config
        pass

    def run(self, data):
        """
        根据输入数据运行设备，参数测量和输出
        :param data: 输入数据
        :return:
        """
        self.data_in = data
        self.measurement.on_measure(self.get_measurement())
        self.output.on_output(self.get_output())

    def get_measurement(self):
        """
        生成测量量
        :return: 由各个测量字段为键的字典
        """
        return self.data_measure

    def get_output(self):
        """
        获取设备输出
        :return:  设备输出json
        """
        return self.data_out
