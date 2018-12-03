# coding = utf-8
# “逆变器频率故障”故障诊断调用模块
from main.src.use.listeners.CommonListener import *
from main.src.application.diagnosis.General import *
import json

# 故障名称
fault_name = '逆变器频率故障'
# 需要的数据，类型：返回时的字段名称
need_data = {'频率': 'freq'}


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
            execute.set_data(float(data['freq']))
            execute.set_execute_listener(CommonListener(self.__identify, self.__socket))
            algorithm = ValueIsOutOfRange()
            algorithm.set_low_threshold(49)
            algorithm.set_high_threshold(51)
            execute.set_algorithm(algorithm)
            execute.execute()
        except json.JSONDecodeError:
            self.__socket.send_json({'token': self.__identify, 'data': {'error': 'json解析错误'}})
