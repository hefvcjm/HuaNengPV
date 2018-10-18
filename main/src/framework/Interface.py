class Formatter:
    """
    数据格式化formatter
    """

    def format(self, data):
        """
        格式化数据
        :param data: 待格式化的数据
        :return: 已经格式化好的数据formatted_data
        """
        pass


class Handler:
    """
    输入数据预处理handler
    """

    def handle(self, data):
        """
        处理数据
        :param data: 待处理的数据
        :return: 处理好的数据handled_data
        """
        pass


class Reviser:
    """
    输出结果修正reviser
    """

    def revise(self, data):
        """
        修正数据
        :param data: 待修正的数据
        :return: 已经修正好的数据revised_data
        """
        pass


class OnExecuteListener:
    """
    执行监听器listener
    """

    def on_success(self, result):
        """
        执行成功回调方法
        :param result: 执行成功后返回的数据
        :return: 无返回
        """
        pass

    def on_failure(self, error):
        """
        执行失败回调方法
        :param error: 失败信息
        :return: 无返回
        """
        pass
