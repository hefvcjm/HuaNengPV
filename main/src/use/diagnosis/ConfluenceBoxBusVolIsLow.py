# coding = utf-8
# “汇流箱母线电压偏低”故障诊断调用模块
from main.src.application.diagnosis.General import *
from main.src.use.listeners.CommonListener import *
import json

# 故障名称
fault_name = '汇流箱母线电压偏低'
# 需要的数据，类型：返回时的字段名称
need_data = {'devType': '汇流箱', 'params': ['voltage']}


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
            execute.set_data(float(data['voltage']))
            execute.set_execute_listener(CommonListener(self.__identify, self.__socket))
            algorithm = ValueIsLow()
            algorithm.set_threshold(0.5)
            execute.set_algorithm(algorithm)
            execute.execute()
        except json.JSONDecodeError:
            self.__socket.send_json({'token': self.__identify, 'data': {'error': 'json解析错误'}})
