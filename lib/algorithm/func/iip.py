# coding = utf-8
from lib.algorithm.IIP.iip import iip


def iip_max_temp(img_path):
    """
    获取红外图像最大温度和区域
    :param img_path: 红外图像路径 [图像路径]
    :return: 最大温度, 区域索引列表
    -----------------------------------------------------
    参数说明如上所述
    触发条件：实时触发
    """
    return iip(img_path).get_max_temp()
