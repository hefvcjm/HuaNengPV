# coding = utf-8
# 逆变器故障诊断
from .config import *


# 逆变器过温
def converter_over_temp(temp, last_result):
    """
    逆变器过温
    :param temp: 逆变器温度
    :param last_result: 上一次判断结果
    :return: 本次判断结果
    """
    if temp < config_converter_over_temp["low_bias"]:
        return False
    if temp > config_converter_over_temp["low_bias"] and last_result:
        return True
    if temp > config_converter_over_temp["high_bias"]:
        return True
    return False


# 逆变器频率故障
def converter_freq_fault(freq):
    """
    逆变器频率故障
    :param freq: 当前频率
    :return: 判断结果，(Boolean，str：under，over and normal)
    """
    if freq < config_converter_freq_fault["low_bias"]:
        return True, "under"
    if freq > config_converter_freq_fault["high_bias"]:
        return True, "over"
    return False, "normal"


# 逆变器交流电压过压或欠压
def converter_voltage_fault(voltage):
    """
    逆变器交流电压过压或欠压
    :param freq: 当前电压
    :return: 判断结果，(Boolean，str：under，over and normal)
    """
    if voltage < config_converter_voltage_fault["low_bias"]:
        return True, "under"
    if voltage > config_converter_voltage_fault["high_bias"]:
        return True, "over"
    return False, "normal"


# 逆变器输出功率偏低
def converter_power_low(power, thr_power):
    """
    逆变器输出功率偏低
    :param power: 功率
    :param thr_power: 理论功率
    :return: 判断结果
    """
    if power < thr_power * config_converter_power_low["rate"]:
        return True
    return False


# 逆变器效率偏低
def converter_efficiency_low(efficiency):
    """
    逆变器效率偏低
    :param efficiency: 效率
    :return: 判断结果
    """
    if efficiency < config_converter_efficiency_low["efficiency"]:
        return True
    return False
