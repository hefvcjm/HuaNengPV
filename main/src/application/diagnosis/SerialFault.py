# 诊断支路故障
from main.src.application.diagnosis.config import *
from .General import *


# 支路电流为零
def serial_current_zero(currents, count):
    """
    支路电流为零
    :param currents: 全部支路电流列表
    :param count: 全部支路上次判断结果各自的累计
    :return: 判断结果列表，累计次数列表
    """
    n = len(currents)
    if list(map(lambda x: x < config_serial_current_zero["zero_bias"], currents)).count(True) \
            < n * config_serial_current_zero["zero_rate"]:
        return compare_low_threshold(currents, count
                                     , config_serial_current_zero["zero_bias"]
                                     , config_serial_current_zero["counter"])
    else:
        return [False] * n, [0] * n


# 支路电流过低
def serial_current_is_low(currents, count, bias):
    """
    支路电流过低
    :param currents: 支路电流列表
    :param count: 上次判断累计列表
    :param bias: 阈值
    :return: 判断结果列表，累计次数列表
    """
    return compare_low_threshold(currents, count, bias, config_serial_current_low["counter"])


# 所有支路电流为零
def serial_current_all_zero(box_current, serial_currents, count):
    """
    所有支路电流为零
    :param box_current: 汇流箱输出电流
    :param serial_currents: 汇流箱输入支路电流列表
    :param count: 上次判断累计
    :return: 判断结果，累计
    """
    if box_current < config_serial_current_all_zero["box_bias"]:
        if list(map(lambda x: x < config_serial_current_all_zero["serial_bias"])).count(True) \
                > len(serial_currents) * config_serial_current_all_zero["serial_rate"]:
            if count > config_serial_current_all_zero["box_counter"]:
                return True, count
            else:
                count += 1
                return False, count
    return False, 0


# 汇流箱母线电压过低
def combiner_box_voltage_low(voltage, count, bias):
    """
    汇流箱母线电压过低
    :param voltage: 汇流箱母线
    :param count: 上次累计次数
    :param bias: 阈值
    :return: 判断结果，累计
    """
    result, count = compare_low_threshold([voltage], [count], bias, config_combiner_box_voltage_low["counter"])
    return result[0], count[0]
