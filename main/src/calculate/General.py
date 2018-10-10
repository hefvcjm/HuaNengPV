# coding=utf-8
"""
计算光伏中的常用变量
"""

STD_TYPE = ('EUROPE', 'CALIFORNIA', 'CHINA')
STD_TYPE_MAP = {
    STD_TYPE[0]: ([0.05, 0.10, 0.20, 0.30, 0.50, 1.0], [0.03, 0.06, 0.13, 0.1, 0.48, 0.2])
    , STD_TYPE[1]: ([0.10, 0.20, 0.30, 0.50, 0.75, 1.0], [0.04, 0.05, 0.12, 0.21, 0.53, 0.05])
    , STD_TYPE[2]: ([0.05, 0.10, 0.20, 0.30, 0.50, 0.75, 1.0], [0.02, 0.03, 0.06, 0.12, 0.25, 0.37, 0.15])}


def pv_conversion_rate(current, voltage, optical_power, pv_cell_area, num):
    """
    计算光电转换率
    :param current: 电流(A)
    :param voltage: 电压(V)
    :param optical_power: 光功率(W/m²)
    :param pv_cell_area: 计算的光伏电池板面积(m²)
    :param num: 光伏电池板个数
    :return:
    """
    if not (isinstance(current, int) or isinstance(current, float)):
        raise Exception("数据类型错误", current)
    if not (isinstance(voltage, int) or isinstance(voltage, float)):
        raise Exception("数据类型错误", voltage)
    if not (isinstance(optical_power, int) or isinstance(optical_power, float)):
        raise Exception("数据类型错误", optical_power)
    if not (isinstance(pv_cell_area, int) or isinstance(pv_cell_area, float)):
        raise Exception("数据类型错误", pv_cell_area)
    if not isinstance(num, int):
        raise Exception("数据类型错误", num)
    if pv_cell_area < 0:
        raise Exception("输入数据范围错误", pv_cell_area)
    if num < 0:
        raise Exception("输入数据范围错误", num)
    return current * voltage / (optical_power * pv_cell_area * num)


def inverter_efficiency(data, std_type=STD_TYPE[0]):
    """
    计算逆变器效率
    :param data: [(负荷率,效率),...]
    :param std_type: 使用标准类型，欧洲效率，加州效率，中国效率..
    :return: 加权后的效率
    """
    if not isinstance(std_type, str):
        raise Exception("数据类型错误", std_type)
    if not isinstance(data, list):
        raise Exception("数据类型错误", std_type)
    if std_type.upper() not in STD_TYPE:
        raise Exception("无该效率计算标准类型", std_type)
    if data is None:
        raise Exception("参数不能为None", data)
    i = 0
    for item in data:
        if not isinstance(item, tuple):
            raise Exception("元素数据类型错误", data[i])
        if len(item) != 2:
            raise Exception("元组需要包含两个元素", data[i])
        if item[0] < 0 or item[0] > 1 or item[1] < 0 or item[1] > 1:
            raise Exception("数据超出合理范围", data[i])
        i = i + 1
    load_rate = STD_TYPE_MAP[std_type][0]
    weight = STD_TYPE_MAP[std_type][1]
    result = 0
    den = 0
    for item in data:
        i = 0
        for rate in load_rate:
            if item[0] < rate:
                break
            i = i + 1
        if i >= len(load_rate):
            i = len(load_rate) - 1
        result = result + item[1] * weight[i]
        den = den + weight[i]
    if den == 0:
        raise Exception("出错")
    return result / den
