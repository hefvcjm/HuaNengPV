# coding = utf-8
"""
本python文件将对光伏发电单元管理系统里面用的的计算进行封装
"""

import numpy as np
import pandas as pd
import math
from lib.algorithm.calc.calculation import calc_generation_in_period
from lib.algorithm.calc.calculation import total_irradiation_in_period
from lib.algorithm.calc.calculation import correction_temp_factor
from lib.algorithm.calc.calculation import ave_cell_temperature


def main_transformer_generation_in_period(time, powers1: list, powers2: list):
    """
    电站在某段时间内的发电量(利用主变数据计算)
    :param time: 时间（格式：yyyy-MM-DD HH:mm:ss）列表，若等间隔则为一个float类型，单位：秒
    :param powers1: 数据库查询time时间列表对应的功率列表[X号主变高压侧测控P]
    :param powers2: 数据库查询time时间列表对应的功率列表[X号主变高压侧测控P1]
    :return: 开始时刻到结束时刻电站的总发电量
    -----------------------------------------------------
    参数说明如上所述
    触发条件：查询触发
    """
    powers = np.array(powers1) + np.array(powers2)
    return calc_generation_in_period(time, powers)


def gather_power_wire_generation_in_period(time, powers: list):
    """
    集电线在某段时间内的发电量
    :param time: 时间（格式：yyyy-MM-DD HH:mm:ss）列表，若等间隔则为一个float类型，单位：秒
    :param powers: 数据库查询time时间列表对应的功率列表[xxxx华能X线保护测控P]
    :return: 开始时刻到结束时刻集电线的总发电量
    -----------------------------------------------------
    参数说明如上所述
    触发条件：查询触发
    """
    return calc_generation_in_period(time, powers)


def inverter_generation_in_period(time, powers: list):
    """
    逆变器在某段时间内的发电量
    :param time: 时间（格式：yyyy-MM-DD HH:mm:ss）列表，若等间隔则为一个float类型，单位：秒
    :param powers: 数据库查询time时间列表对应的功率列表[#X光伏子阵X#逆变器输出总有功]
    :return: 开始时刻到结束时刻集电线的总发电量
    -----------------------------------------------------
    参数说明如上所述
    触发条件：查询触发
    """
    return calc_generation_in_period(time, powers)


def box_generation_in_period(time, voltages: list, *currents):
    """
    汇流箱在某段时间内的发电量
    :param time: 时间（格式：yyyy-MM-DD HH:mm:ss）列表，若等间隔则为一个float类型，单位：秒
    :param voltages: 数据库查询time时间列表对应的汇流箱总电压列表[#X光伏子阵汇流箱X汇流总电压]
    :param currents: 数据库查询time时间列表对应的汇流箱各路电流列表[#X光伏子阵汇流箱X IX]
    :return: 起始时刻到结束时刻汇流箱的发电量
    -----------------------------------------------------
    参数说明如上所述
    说明：currents为汇流箱的全部电流列表，一路对应一个参数，
          假如有1路，调用则为box_generation_in_period(time, voltages, current1)
          假如有3路，调用则为box_generation_in_period(time, voltages, current1, current2, current3)
          以此类推，currenti为各路电流列表
    触发条件：查询触发
    """
    powers = np.array(voltages) * np.array(currents).sum(axis=1)
    return calc_generation_in_period(time, powers)


def series_generation_in_period(time, voltages: list, currents: list):
    """
    组串在某段时间内的发电量
    :param time: 时间（格式：yyyy-MM-DD HH:mm:ss）列表，若等间隔则为一个float类型，单位：秒
    :param voltages: 数据库查询time时间列表对应的汇流箱总电压列表[#X光伏子阵汇流箱X汇流总电压]
    :param currents: 数据库查询time时间列表对应的汇流箱各路电流列表[#X光伏子阵汇流箱X IX]
    :return: 起始时刻到结束时刻组串的发电量
    -----------------------------------------------------
    参数说明如上所述
    触发条件：查询触发
    """
    powers = np.array(voltages) * np.array(currents)
    return calc_generation_in_period(time, powers)


def year_plan_completion_rate(real_gen: float, plan_gen: float):
    """
    年计划发电完成度
    :param real_gen: 年初到现在实际发电量[先调用main_transformer_generation_in_period函数计算得到]
    :param plan_gen: 年计划发电量
    :return: 年计划发电完成度
    -----------------------------------------------------
    参数说明如上所述
    触发条件：定时触发（天）
    """
    return real_gen / plan_gen


def device_theoretical_generation(time, irradiation: list, temps: list, delta: float, gstc: float, p0: float,
                                  mu: float, ):
    """
    某段时间某设备的理论发电量
    :param time: 时间（格式：yyyy-MM-DD HH:mm:ss）列表，若等间隔则为一个float类型，单位：秒
    :param irradiation: 与时间列表对应的辐照度数据 [光功率预测遥测直辐射瞬时值]
    :param temps: 对应时间的光伏组件背板温度  [光功率预测遥测组件温度]
    :param delta: 光伏组件的功率温度系数，由组件铭牌参数得到 [光伏组件的功率温度系数]
    :param gstc: gstc1000W/m² [参数表：id=9,name=标准辐照度]
    :param p0: 某设备的装机容量，kW [装机容量]
    :param mu: 光伏组件年衰减系数 [参数表：name=XXX站#XX逆变器组件年衰减率]
    :return: 起始时刻到终止时刻设备的理论发电量
    -----------------------------------------------------
    参数说明如上所述
    触发条件：查询触发
    """
    total_irr = total_irradiation_in_period(time, irradiation)
    return (total_irr / gstc) * p0 * mu * correction_temp_factor(delta, ave_cell_temperature(time, temps))


def device_pr_in_period(real_gen: float, theoretical_gen: float):
    """
    某段时间设备pr
    :param real_gen: 实际发电量
    :param theoretical_gen: 理论发电量
    :return: 某段时间设备pr
    -----------------------------------------------------
    real_gen：先调用前面函数得到该数
              电站发电量：main_transformer_generation_in_period
              集电线：gather_power_wire_generation_in_period
              逆变器：inverter_generation_in_period
              汇流箱：box_generation_in_period
              组串：serials_generation_in_period
    theoretical_gen：调用device_theoretical_generation得到结果
    触发条件：定时触发（天）+ 查询触发
    """
    return real_gen / theoretical_gen


def square_loss_in_period(square_theoretical_gen: float, inverters_gen: list):
    """
    某段时间方阵的吸收损耗
    :param square_theoretical_gen: 某段时间内方阵的理论发电量
    :param inverters_gen: 某段时间内方阵下逆变器的实际发电量列表
    :return: 某段时间方阵的吸收损耗
    -----------------------------------------------------
    square_theoretical_gen：调用device_theoretical_generation得到结果
    inverters_gen：调用inverter_generation_in_period得到方阵下逆变器发电量，形成一个列表传进来
    触发条件：查询触发
    """
    return square_theoretical_gen - sum(inverters_gen)


def inverter_limit_power_loss_in_period(std_inverter_gen: float, limit_inverter_gen: float):
    """
    某段时间逆变器的限电损耗
    :param std_inverter_gen: 某段时间标杆逆变器发电量
    :param limit_inverter_gen: 某段时间限电逆变器发电量
    :return: 逆变器限电损耗
    -----------------------------------------------------
    std_inverter_gen：调用inverter_generation_in_period计算标杆方阵下逆变器发电量
    limit_inverter_gen：调用inverter_generation_in_period计算非标杆方阵下逆变器发电量
    触发条件：查询触发，标杆方阵为几个固定方阵，限电逆变器有查询是选择确定
    """
    return std_inverter_gen - limit_inverter_gen


def inverter_fault_stop_loss_in_period(std_inverter_gen: float, fault_inverter_gen: float):
    """
    某段时间逆变器故障停机损耗
    :param std_inverter_gen: 某段时间标杆逆变器发电量
    :param fault_inverter_gen: 某段时间故障停机逆变器发电量
    :return: 某段时间逆变器故障停机损耗
    -----------------------------------------------------
    std_inverter_gen：调用inverter_generation_in_period计算标杆方阵下逆变器发电量
    fault_inverter_gen：调用inverter_generation_in_period计算故障停机逆变器逆变器发电量
    触发条件：查询触发，标杆方阵为几个固定方阵，故障停机逆变器有查询是选择确定
    """
    return std_inverter_gen - fault_inverter_gen


def inverter_fix_stop_loss_in_period(std_inverter_gen: float, fix_inverter_gen: float):
    """
    某段时间逆变器检修停机损耗
    :param std_inverter_gen: 某段时间标杆逆变器发电量
    :param fix_inverter_gen: 某段时间检修停机逆变器发电量
    :return: 某段时间逆变器检修停机损耗
    -----------------------------------------------------
    std_inverter_gen：调用inverter_generation_in_period计算标杆方阵下逆变器发电量
    fix_inverter_gen：调用inverter_generation_in_period计算检修停机逆变器逆变器发电量
    触发条件：查询触发，标杆方阵为几个固定方阵，检修停机逆变器有查询是选择确定
    """
    return std_inverter_gen - fix_inverter_gen


def zero_series_loss_in_period(num: int, normal_series_gen: list):
    """
    某段时间汇流箱零支路损耗
    :param num: 汇流箱零支路数
    :param normal_series_gen: 某段时间正常支路发电量列表
    :return: 某段时间汇流箱零支路损耗
    -----------------------------------------------------
    num：某段时间某汇流箱零电流支路数，由故障列表统计得出，即发生[支路电流为零]的支路数
    normal_series_gen：设备某段时间实际发电量，由serials_generation_in_period函数计算该数值
    触发条件：查询触发
    """
    return num / len(normal_series_gen) * sum(normal_series_gen)


def inverter_loss_in_period(time, powers_out: list, powers_in: list):
    """
    某段时间逆变器损耗
    :param time: 时间（格式：yyyy-MM-DD HH:mm:ss）列表，若等间隔则为一个float类型，单位：秒
    :param powers_out: 数据库查询time时间列表对应的功率列表[#X光伏子阵X#逆变器输出总有功]
    :param powers_in: 数据库查询time时间列表对应的功率列表[#X光伏子阵X#逆变器PV输入功率]
    :return: 某段时间逆变器损耗
    -----------------------------------------------------
    参数说明如上所述
    触发条件：查询触发
    """
    powers = np.array(powers_in) - np.array(powers_out)
    return calc_generation_in_period(time, powers)


def other_loss_in_period(square_loss: float, other: list):
    """
    某段时间其他损耗
    :param square_loss: 某段时间方阵吸收损耗[square_loss_in_period计算得到]
    :param other: 某段时间确定的损耗列表
                  [inverter_limit_power_loss_in_period,
                  inverter_fault_stop_loss_in_period,
                  inverter_fix_stop_loss_in_period,
                  zero_series_loss_in_period,
                  inverter_loss_in_period]计算结果组成的列表
    :return: 某段时间其他损耗
    -----------------------------------------------------
    参数说明如上所述
    触发条件：查询触发
    """
    return square_loss - sum(other)


def aging_rate(before: float, arfa: float, daily_healths: list):
    """
    设备年老化率，结果保存
    :param before: 前一年老化率
    :param arfa: 老化系数
    :param daily_healths: 年每日健康度(%)
    :return: 今年老化率
    -----------------------------------------------------
    before：前一年老化率，查询历史结果
    arfa： 配置参数[name=XX站组串老化系数-arfa]
    daily_healths：某设备健康度列表
    触发条件：定时触发（年）
    """
    return before - arfa * sum(map(lambda x: 1 - x, daily_healths))
