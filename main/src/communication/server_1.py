import zmq
import json
from main.src.framework.Execute import *
import copy
from main.src.communication.FunctionMapping import *

context = zmq.Context()
socket = context.socket(zmq.REP)
# REP连接的是DEALER
socket.connect("tcp://localhost:5560")


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


while True:
    message = socket.recv()
    print("server received: %s" % message.decode('utf-8'))
    try:
        json_msg = json.loads(message.decode())
        if 'target' in json_msg.keys() and 'function' in json_msg.keys():
            if json_msg['target'] == 'require algorithm':
                path = FUNCTION_MAPPING[json_msg['function']]
                print(path)
                if path is not None:
                    obj = __import__(path, fromlist=True)
                    method = getattr(obj, 'main')
                    method(socket)
    except json.JSONDecodeError:
        socket.send({'error': 'json解析错误'})
