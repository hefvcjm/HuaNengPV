# coding = utf-8
# 该文件封装数据协议相关的处理程序
# 包括对数据的解析和封装
import json


def parse(data):
    """
    解析接收到的数据
    :param data: 接收到的数据
    :return: 解析结果
    """
    if data["type"] == "trigger":
        pass