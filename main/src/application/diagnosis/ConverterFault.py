# coding = utf-8
# 逆变器故障诊断
from .config import *


# 逆变器过温
def converter_over_temp(temp, last_result, config=config_converter_over_temp):
    """
    逆变器过温
    :param temp: 逆变器温度
    :param last_result: 上一次判断结果
    :param config: 配置信息
    :return: 本次判断结果
    """
    if temp < config["low_bias"]:
        return False
    if temp > config["low_bias"] and last_result:
        return True
    if temp > config["high_bias"]:
        return True
    return False


# 逆变器频率故障
def converter_freq_fault(freq, config=config_converter_freq_fault):
    """
    逆变器频率故障
    :param freq: 当前频率
    :param config: 配置信息
    :return: 判断结果，(Boolean，str：under，over and normal)
    """
    if freq < config["low_bias"]:
        return True, "under"
    if freq > config["high_bias"]:
        return True, "over"
    return False, "normal"


# 逆变器交流电压过压或欠压
def converter_voltage_fault(voltage, config=config_converter_voltage_fault):
    """
    逆变器交流电压过压或欠压
    :param voltage: 当前电压
    :param config: 配置信息
    :return: 判断结果，(Boolean，str：under，over and normal)
    """
    if voltage < config["low_bias"]:
        return True, "under"
    if voltage > config["high_bias"]:
        return True, "over"
    return False, "normal"


# 逆变器输出功率偏低
def converter_power_low(power, thr_power, config=config_converter_power_low):
    """
    逆变器输出功率偏低
    :param power: 功率
    :param thr_power: 理论功率
    :param config: 配置信息
    :return: 判断结果
    """
    if power < thr_power * config["rate"]:
        return True
    return False


# 逆变器效率偏低
def converter_efficiency_low(efficiency, config=config_converter_efficiency_low):
    """
    逆变器效率偏低
    :param efficiency: 效率
    :param config: 配置信息
    :return: 判断结果
    """
    if efficiency < config["efficiency"]:
        return True
    return False


# 逆变器损耗过高
def converter_loss_high(loss, config=config_converter_loss_high):
    """
    逆变器损耗过高
    :param loss: 当前损耗
    :param config: 配置信息
    :return: 判断结果
    """
    if loss > config["threshold"]:
        return True
    return False
