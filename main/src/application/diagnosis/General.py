# coding=utf-8
from main.src.framework.BaseAlgorithm import *


class ValueIsZero(BaseAlgorithm):
    """
    判断某个量是否为零。
    可以利用set_count()和set_error()来设置连续次数和判断偏差大小，否则取默认值。
    输入：连续输入某个量。
    输入：判断连续几次为零后输出True，否则输出False。
    可以诊断故障类型：某一支路电流为零、所有支路电流为零。
    """
    # 默认连续次数
    __count = 5
    # 默认误差
    __error = 0.01
    # 用来累计已经连续电流为0的次数
    __add_up = 0
    # 结果
    __result = False

    def __init__(self):
        super().__init__()

    def set_count(self, count):
        # 不能小于1
        if count >= 1:
            self.__count = count

    def set_error(self, error):
        # 不能小于0
        if error > 0:
            self.__error = error

    def set_add_up(self, add_up):
        # 不能小于0
        if add_up > 0:
            self.__add_up = add_up

    def get_add_up(self):
        return self.__add_up

    def run(self):
        super().run()
        if self._data < self.__error:
            self.__add_up += 1
        else:
            self.__add_up = 0
        if self.__add_up >= self.__count:
            self.__add_up = self.__count
            self.__result = True
        else:
            self.__result = False
        self._on_execute_listener.on_success((self.__result, self.__add_up))


class ValueIsLow(BaseAlgorithm):
    """
    判断某个量是是否偏低。
    可以利用set_threshold()设置阈值。
    输入：输入某个量。
    输入：偏低输出True，否则输出False。
    可以诊断故障类型：支路电流偏低、汇流箱母线电压偏低、逆变器交流欠压、逆变器输出功率偏低、逆变器效率偏低。
    """
    # 阈值
    __threshold = None
    # 结果
    __result = False

    def __init__(self):
        super().__init__()

    def set_threshold(self, threshold):
        self.__threshold = threshold

    def run(self):
        super().run()
        if self.__threshold is None:
            return
        if self._data < self.__threshold:
            self.__result = True
        else:
            self.__result = False
        self._on_execute_listener.on_success(self.__result)


class ValueIsHigh(BaseAlgorithm):
    """
    判断某个量是是否偏高。
    可以利用set_threshold()设置阈值。
    输入：输入某个量。
    输入：偏高输出True，否则输出False。
    可以诊断故障类型：逆变器过温、逆变器交流过压、逆变器直流过压、逆变器损耗过高。
    """
    # 阈值
    __threshold = None
    # 结果
    __result = False

    def __init__(self):
        super().__init__()

    def set_threshold(self, threshold):
        self.__threshold = threshold

    def run(self):
        super().run()
        if self.__threshold is None:
            return
        if self._data > self.__threshold:
            self.__result = True
        else:
            self.__result = False
        self._on_execute_listener.on_success(self.__result)


class ValueIsOutOfRange(BaseAlgorithm):
    """
    判断某个量是是否偏高。
    可以利用set_high_threshold()和set_low_threshold()设置上下阈值。
    输入：输入某个量。
    输入：偏高输出1，偏低输出-1，否则输出0。
    可以诊断故障类型：逆变器交流频率故障。
    """
    # 下阈值
    __low_threshold = None
    # 上阈值
    __high_threshold = None
    # 结果
    __result = False

    def __init__(self):
        super().__init__()

    def set_low_threshold(self, threshold):
        self.__low_threshold = threshold

    def set_high_threshold(self, threshold):
        self.__high_threshold = threshold

    def run(self):
        super().run()
        if self.__low_threshold is None or self.__high_threshold is None:
            return
        if self._data < self.__low_threshold:
            self.__result = -1
        elif self._data > self.__high_threshold:
            self.__result = 1
        else:
            self.__result = 0
        self._on_execute_listener.on_success(self.__result)
