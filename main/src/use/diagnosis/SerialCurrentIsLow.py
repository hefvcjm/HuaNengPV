# -*- coding: UTF-8 -*-
# “支路电流偏低”故障诊断调用模块
from main.src.use.listeners.CommonListener import *
from main.src.application.diagnosis.General import *
import json

# 故障名称
fault_name = '支路电流偏低'
# 需要的数据，类型：返回时的字段名称
need_data = [{"devType": "支路", "params": ["current", "count"]}]


class Application:
    __data = None
    __socket = None
    __identify = None

    def __init__(self, identify, socket):
        self.__socket = socket
        self.__identify = identify
        socket.send_json({'type': 'request', 'token': identify, 'device': need_data})

    def main(self, data):
        self.__data = data
        print(fault_name + " Received request: %s" % data)
        try:
            execute = Execute()
            execute.set_data(float(data['current']))
            execute.set_execute_listener(CommonListener(self.__identify, self.__socket))
            algorithm = ValueIsLow()
            algorithm.set_threshold(0.5)
            execute.set_algorithm(algorithm)
            execute.execute()
        except json.JSONDecodeError:
            self.__socket.send_json({'token': self.__identify, 'data': {'error': 'json解析错误'}})
