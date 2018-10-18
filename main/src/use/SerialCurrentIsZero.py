# coding = utf-8
# “某一支路电流为零”故障诊断调用模块
"""
触发算法
    -->
    {
        'target'：'require algorithm',
        'function':'某一支路电流为零'
    }

    返回示例
    其中，key为数据说明，value为调用出返回时该数据的key
    <--
    {
        '电流': 'current',
        '累计次数': 'count'
    }

返回请求数据示例
其中count为上一次结果附带需要保存的变量
    -->
    {
        'current':1.5648,
        'count':3
    }

算法结果返回数据示例
    <--
    {
        'result': False,
        'count': 0
    }

"""
from main.src.framework.Execute import *
from main.src.application.diagnosis.General import *
import json

# 需要的数据，类型：返回时的字段名称
need_data = {'电流': 'current', '累计次数': 'count'}


class ResultFormatter(Formatter):
    """
    默认输出结果格式化formatter
    """

    def format(self, data):
        return {'result': data[0], 'count': data[1]}


class ExecuteListener(OnExecuteListener):
    __socket = None

    def __init__(self, socket):
        self.__socket = socket

    def on_success(self, result):
        print(result)
        self.__socket.send(str(result).encode())

    def on_failure(self, error):
        print(error)
        self.__socket.send(str(error).encode())


def main(socket):
    socket.send_json(need_data)
    message = socket.recv()
    print("某一支路电流为零 Received request: %s" % message.decode())
    try:
        json_msg = json.loads(message.decode())
        execute = Execute()
        execute.set_data(float(json_msg['current']))
        execute.set_execute_listener(ExecuteListener(socket))
        execute.set_formatter(None, ResultFormatter())
        algorithm = ValueIsZero()
        algorithm.set_add_up(int(json_msg['count']))
        execute.set_algorithm(algorithm)
        execute.execute()
    except json.JSONDecodeError:
        socket.send({'error': 'json解析错误'})
