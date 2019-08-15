# coding = utf-8
"""
本python文件将对光伏发电单元管理系统里面用的的计算进行封装
"""

import numpy as np
import pandas as pd
import math


def station_total_generation(meas: float, factor: float):
    """
    计算电站总发电量，该结果需要进行库存
    :param meas: 上网电线电度表测量的电量数据
    :param factor: 计量关口系数
    :return: 电站总发电量
    """
    return meas * factor


def station_generation_in_period(start_gen: float, end_gen: float):
    """
    电站在某段时间内的发电量
    :param start_gen: 开始时刻的电站总发电量（查询数据库获取）
    :param end_gen: 结束时刻电站的总发电量（查询数据库获取）
    :return: 开始时刻到结束时刻电站的总发电量
    """
    return end_gen - start_gen


def gather_power_wire_generation(meas: float, factor: float):
    """
    计算集电线总发电量，该结果需要进行库存
    :param meas: 集电线电度表测量的电量数据
    :param factor: 计量关口系数
    :return: 集电线总发电量
    """
    return meas * factor


def gather_power_wire_generation_in_period(start_gen: float, end_gen: float):
    """
    集电线在某段时间内的发电量
    :param start_gen: 开始时刻的集电线总发电量（查询数据库获取）
    :param end_gen: 结束时刻集电线的总发电量（查询数据库获取）
    :return: 开始时刻到结束时刻集电线的总发电量
    """
    return end_gen - start_gen


def inverter_generation_in_period(start_gen: float, end_gen: float):
    """
    逆变器在某段时间内的发电量
    :param start_gen: 开始时刻的逆变器总发电量（查询数据库获取）
    :param end_gen: 结束时刻逆变器的总发电量（查询数据库获取）
    :return: 开始时刻到结束时刻逆变器的总发电量
    """
    return end_gen - start_gen


def box_generation_in_period(time, powers: list):
    """
    汇流箱在某段时间内的发电量
    :param time: 时间（格式：yyyy-MM-DD HH:mm:ss）列表，若等间隔则为一个float类型，单位：秒
    :param powers: 对应时间列表的功率列表,单位：kW/h
    :return: 起始时刻到结束时刻汇流箱的发电量
    """
    if type(time) == float:
        return (sum(powers[1:] + powers[:-1]) / 2) * time / 3600
    return pd.to_datetime(pd.Series(time)).diff().dropna().map(
        lambda x: x.value / 10 ** 6 / 1000 / 3600).values @ ((np.array(powers[:-1]) + np.array(powers[1:])) / 2)


def series_generation_in_period(time, box_powers: list, box_currents: list, series_currents: list):
    """
    组串在某段时间内的发电量
    :param time: 时间（格式：yyyy-MM-DD HH:mm:ss）列表，若等间隔则为一个float类型，单位：秒
    :param box_powers: 对应时间列表汇流箱的功率列表,单位：kW/h
    :param box_currents: 对应时间列表汇流箱的输出电流列表,单位：kW/h
    :param series_currents: 对应时间列表汇流箱某路组串的电流，单位：A
    :return: 起始时刻到结束时刻组串的发电量
    """
    if type(time) == float:
        powers = np.array(box_powers) / np.array(box_currents) * np.array(series_currents)
        return (sum(powers[1:] + powers[:-1]) / 2) * time / 3600
    powers = np.array(box_powers) / np.array(box_currents) @ np.array(series_currents)
    return (pd.to_datetime(pd.Series(time)).diff().dropna().map(
        lambda x: x.value / 10 ** 6 / 1000 / 3600).values @ ((powers[:-1] + powers[1:]) / 2))


def year_plan_completion_rate(year_start_gen: float, now_gen: float, plan_gen: float):
    """
    年计划发电完成度
    :param year_start_gen: 年初电站总发电量（数据库查询获得）
    :param now_gen: 当前电站总发电量
    :param plan_gen: 年计划发电量
    :return: 年计划发电完成度
    """
    return (now_gen - year_start_gen) / plan_gen


def total_irradiation_in_period(time, irradiation: list):
    """
    某段时间累计辐照度
    :param time: 时间（格式：yyyy-MM-DD HH:mm:ss）列表，若等间隔则为一个float类型，单位：秒
    :param irradiation: 与时间列表对应的辐照度数据
    :return: 起始时刻到终止时刻的累计辐照度
    """
    if type(time) == float:
        return (sum(irradiation[1:] + irradiation[:-1]) / 2) * time / 3600
    return (pd.to_datetime(pd.Series(time)).diff().dropna().map(
        lambda x: x.value / 10 ** 6 / 1000 / 3600).values @ (
                    (np.array(irradiation[:-1]) + np.array(irradiation[1:])) / 2))


def device_theoretical_generation(total_irr: float, gstc: float, p0: float, mu: float, c: float):
    """
    某段时间某设备的理论发电量
    :param total_irr: 某段时间的累计辐照度 kWh/m²
    :param gstc: 标准辐照度1000W/m²
    :param p0: 某设备的装机容量，kW
    :param mu: 光伏组件年衰减系数
    :param c: 温度修正系数
    :return: 起始时刻到终止时刻设备的理论发电量
    """
    return (total_irr / gstc) * p0 * mu * c


def ave_cell_temperature(time, temps: list):
    """
    某段时间内光伏组件电池平均结温
    :param time: 时间（格式：yyyy-MM-DD HH:mm:ss）列表，若等间隔则为一个float类型，单位：秒
    :param temps: 对应时间的光伏组件背板温度
    :return: 起始时刻到终止时刻光伏电池平均结温
    """
    if type(time) == float:
        return np.array(temps[1:] + temps[:-1]).mean() / 2
    delta_time = pd.to_datetime(pd.Series(time)).diff().dropna().map(lambda x: x.value / 10 ** 6 / 1000 / 3600).values
    return (delta_time @ ((np.array(temps[:-1]) + np.array(temps[1:])) / 2)) / delta_time.sum()


def correction_temp_factor(delta: float, t_cell: float):
    """
    温度修正系数
    :param dilta: 光伏组件的功率温度系数，由组件铭牌参数得到
    :param t_cell: 某段时间内光伏组件电池平均结温
    :return: 修正号的温度系数
    """
    return 1 + delta * (t_cell - 25)


def pr_in_period(real_gen: float, theoretical_gen: float):
    """
    某段时间设备pr
    :param real_gen: 实际发电量
    :param theoretical_gen: 理论发电量
    :return: 某段时间设备pr
    """
    return real_gen / theoretical_gen


def square_loss_in_period(square_theoretical_gen: float, inverters_gen: list):
    """
    某段时间方阵的吸收损耗
    :param square_theoretical_gen: 某段时间内方阵的理论发电量
    :param inverters_gen: 某段时间内方阵下逆变器的实际发电量列表
    :return: 某段时间方阵的吸收损耗
    """
    return square_theoretical_gen - sum(inverters_gen)


def inverter_limit_power_loss_in_period(std_inverter_gen: float, limit_inverter_gen: float):
    """
    某段时间逆变器的限电损耗
    :param std_inverter_gen: 某段时间标杆逆变器发电量
    :param limit_inverter_gen: 某段时间限电逆变器发电量
    :return: 逆变器限电损耗
    """
    return std_inverter_gen - limit_inverter_gen


def inverter_fault_stop_loss_in_period(std_inverter_gen: float, fault_inverter_gen: float):
    """
    某段时间逆变器故障停机损耗
    :param std_inverter_gen: 某段时间标杆逆变器发电量
    :param fault_inverter_gen: 某段时间故障停机逆变器发电量
    :return: 某段时间逆变器故障停机损耗
    """
    return std_inverter_gen - fault_inverter_gen


def inverter_fix_stop_loss_in_period(std_inverter_gen: float, fix_inverter_gen: float):
    """
    某段时间逆变器检修停机损耗
    :param std_inverter_gen: 某段时间标杆逆变器发电量
    :param fix_inverter_gen: 某段时间检修停机逆变器发电量
    :return: 某段时间逆变器检修停机损耗
    """
    return std_inverter_gen - fix_inverter_gen


def zero_series_loss_in_period(num: int, normal_series_gen: list):
    """
    某段时间汇流箱零支路损耗
    :param num: 汇流箱零支路数
    :param normal_series_gen: 某段时间正常支路发电量列表
    :return: 某段时间汇流箱零支路损耗
    """
    return num / len(normal_series_gen) * sum(normal_series_gen)


def inverter_loss_in_period(inverter_out: float, inverter_in: float):
    """
    某段时间逆变器损耗
    :param inverter_out: 某段时间逆变器输出电量
    :param inverter_in: 某段时间逆变器输入电流
    :return: 某段时间逆变器损耗
    """
    return inverter_in - inverter_out


def inverter_in_in_period(time, currents: np.array, voltages: np.array):
    """
    某段时间逆变器输入电量
    :param time: 时间（格式：yyyy-MM-DD HH:mm:ss）列表，若等间隔则为一个float类型，单位：秒
    :param currents: 各路输入电流，每一行表示一路，每一列与时间对应
    :param voltages: 各路输入电压，每一行表示一路，每一列与时间对应
    :return: 某段时间逆变器输入电量
    """
    powers = np.sum(currents * voltages, axis=0)
    powers = (powers[1:] + powers[:-1]) / 2
    if type(time) == float:
        return powers * time / 3600
    return pd.to_datetime(pd.Series(time)).diff().dropna().map(
        lambda x: x.value / 10 ** 6 / 1000 / 3600).values @ powers


def other_loss_in_period(square_loss: float, other: list):
    """
    某段时间其他损耗
    :param square_loss: 某段时间方阵吸收损耗
    :param other: 某段时间确定的损耗列表
    :return: 某段时间其他损耗
    """
    return square_loss - sum(other)


def fault_score(x: int, mu: float, sigma: float, M: float, a: int):
    """
    故障评分
    :param x: 某段时间故障次数
    :param mu: 高斯分布均值
    :param sigma: 高斯分布标准差
    :param M: 最低评分
    :param a: 最低评分分界点
    :return: 故障百分制评分(%)
    """
    return math.e ** (-((x - mu) / sigma) ** 2) if x <= a else M


def efficiency_score(x: float, arfa: float, belta: float, M: float, a: float, b: float):
    """
    效率评分
    :param x: 某段时间平均效率
    :param arfa: 偏大型柯西分布隶属函数参数
    :param belta: 偏大型柯西分布隶属函数参数
    :param M: 最低评分
    :param a: 上分界点
    :param b: 下分界点
    :return: 效率百分制评分(%)
    """
    if x > a:
        return 1
    if x < b:
        return M
    return 1 / (1 + arfa * (x - a) ** belta)


def temperature_score(x: float, sigma: float, M: float, a: float, b: float, c: float, d: float):
    """
    温度评分
    :param x: 某段时间平均温度
    :param sigma: 高斯分布标准差
    :param M: 最低评分
    :param a: 第一个分界点
    :param b: 第二个分界点
    :param c: 第三个分界点
    :param d: 第四个分界点
    :return: 温度百分制评分(%)
    """
    if x < a:
        return M
    if x < b:
        return math.e ** (-((x - b) / sigma) ** 2)
    if x < c:
        return 1
    if x < d:
        return math.e ** (-((x - c) / sigma) ** 2)
    return M


def group_health(group_scores: list):
    """
    某段时间设备群健康度
    :param group_scores: 某段时间设备群健康度列表
    :return: 某段时间设备群健康度
    """
    return sum(group_scores) / len(group_scores)


def aging_rate(before: float, arfa: float, daily_healths: list):
    """
    设备年老化率
    :param before: 前一年老化率
    :param arfa: 老化系数
    :param daily_healths: 年每日健康度(%)
    :return: 今年老化率
    """
    return before - arfa * sum(map(lambda x: 1 - x, daily_healths))

