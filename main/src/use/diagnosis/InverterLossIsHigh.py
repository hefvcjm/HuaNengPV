# -*- coding: UTF-8 -*-
# “逆变器损耗过高”故障诊断调用模块
"""
触发算法
    -->
    {
        'target'：'require algorithm',
        'function':'故障诊断'，
        'detail':{
            'type':'逆变器损耗过高'
        }
    }

    返回示例
    其中，key为数据说明，value为调用出返回时该数据的key
    <--
    {
        '输入功率': 'input',
        '输出功率':'output'
    }

返回请求数据示例
其中count为上一次结果附带需要保存的变量
    -->
    {
        'target'：'set data',
        'function':'故障诊断',
        'data':{
            'input':700
            'output':682
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
fault_name = '逆变器损耗过高'
# 需要的数据，类型：返回时的字段名称
need_data = {'输入功率': 'input', '输出功率': 'output'}


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
            execute.set_data(float(data['output']) - float(data['input']))
            execute.set_execute_listener(ExecuteListener(self.__identify, self.__socket))
            algorithm = ValueIsHigh()
            algorithm.set_threshold(20)
            execute.set_algorithm(algorithm)
            execute.execute()
        except json.JSONDecodeError:
            self.__socket.send_json({'token': self.__identify, 'data': {'error': 'json解析错误'}})
