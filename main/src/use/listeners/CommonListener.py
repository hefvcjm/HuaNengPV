# coding=utf-8
# 常规的listener的实现
from main.src.framework.Execute import *
from main.src.communication.FunctionMapping import *


class CommonListener(OnExecuteListener):
    __socket = None
    __identify = None

    def __init__(self, identify, socket):
        self.__identify = identify
        self.__socket = socket

    def on_success(self, result):
        print(result)
        self.__socket.send_json({'type': 'result', 'token': self.__identify, 'data': result})
        try:
            del ID_CLASS_MAPPING[self.__identify]
            print('算法执行完成，删除token为<' + self.__identify + '>对应的算法实例')
        except:
            pass

    def on_failure(self, error):
        print(error)
        self.__socket.send_json({'type': 'error', 'token': self.__identify, 'data': error})
