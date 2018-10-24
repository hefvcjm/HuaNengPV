# coding = utf-8
# “预测组串光电转化率”故障诊断调用模块
from main.src.framework.Execute import *
import json
from main.src.application.predication.PredictionURL import *

# 功能名称
func_name = '预测组串光电转化率'
# 需要的数据，类型：返回时的字段名称
need_data = {'光电转化率': 'conversion'}


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
        socket.send_json({'type': 'request', 'token': identify, 'device': need_data})

    def main(self, data):
        self.__data = data
        print(func_name + " Received request: %s" % data)
        try:
            execute = Execute()
            # 设置数据
            execute.set_data((data['conversion'], 18))
            # 设置监听器
            execute.set_execute_listener(ExecuteListener(self.__identify, self.__socket))
            # 设置执行需要执行的算法
            execute.set_algorithm(PvCellUrlPrediction())
            # 执行
            execute.execute()
        except json.JSONDecodeError:
            self.__socket.send_json({'token': self.__identify, 'data': {'error': 'json解析错误'}})
