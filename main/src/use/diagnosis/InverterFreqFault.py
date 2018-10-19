# coding = utf-8
# “逆变器频率故障”故障诊断调用模块
"""
触发算法
    -->
    {
        'target'：'require algorithm',
        'function':'故障诊断'，
        'detail':{
            'type':'逆变器频率故障'
        }
    }

    返回示例
    其中，key为数据说明，value为调用出返回时该数据的key
    <--
    {
        '频率': 'freq'
    }

返回请求数据示例
    -->
    {
        'target'：'set data',
        'function':'故障诊断',
        'data':{
            'freq':50.32
        }
    }

算法结果返回数据示例
    <--
    {
        'result': False
    }
"""
from main.src.framework.Execute import *
from main.src.application.diagnosis.General import *
import json

# 故障名称
fault_name = '逆变器频率故障'
# 需要的数据，类型：返回时的字段名称
need_data = {'频率': 'freq'}


class ExecuteListener(OnExecuteListener):
    __socket = None
    __identify = None

    def __init__(self, identify, socket):
        self.__identify = identify
        self.__socket = socket

    def on_success(self, result):
        print(result)
        self.__socket.send_json({'token': self.__identify, 'data': {'result': result}})

    def on_failure(self, error):
        print(error)
        self.__socket.send_json({'token': self.__identify, 'data': {'error': error}})


class Application:
    __data = None
    __socket = None
    __identify = None

    def __init__(self, identify, socket):
        self.__socket = socket
        self.__identify = identify
        socket.send_json({'token': self.__identify, 'format': need_data})

    def main(self, data):
        self.__data = data
        print(fault_name + " Received request: %s" % data)
        try:
            execute = Execute()
            execute.set_data(float(data['freq']))
            execute.set_execute_listener(ExecuteListener(self.__identify, self.__socket))
            algorithm = ValueIsOutOfRange()
            algorithm.set_low_threshold(49)
            algorithm.set_high_threshold(51)
            execute.set_algorithm(algorithm)
            execute.execute()
        except json.JSONDecodeError:
            self.__socket.send_json({'token': self.__identify, 'data': {'error': 'json解析错误'}})
