import zmq
import json
from main.src.communication.FunctionMapping import *

port = "5560"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://localhost:%s" % port)
while True:
    #  Wait for next request from client
    message = socket.recv()
    print(message)
    print("server received: %s" % message.decode('utf-8'))
    try:
        json_msg = json.loads(message.decode())
        if 'target' in json_msg.keys() and 'function' in json_msg.keys():
            if json_msg['target'] == 'require algorithm':
                path = DIAGNOSIS_FUNCTION_MAPPING[json_msg['function']]
                print(path)
                if path is not None:
                    obj = __import__(path, fromlist=True)
                    method = getattr(obj, 'main')
                    method(socket)
    except json.JSONDecodeError:
        socket.send({'error': 'json解析错误'})
