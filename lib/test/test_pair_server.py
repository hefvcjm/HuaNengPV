# coding = utf-8
import zmq
import time
import inspect

funcs = {}

base_diagnosis_path = 'lib.algorithm.calculation'
obj = __import__(base_diagnosis_path, fromlist=base_diagnosis_path.split('.'))
# print(getattr(obj, "station_total_generation")(10, 10))
# print(dir(obj))
# print([i for i in dir(obj) if callable(getattr(obj, i))])
for i in dir(obj):
    if callable(getattr(obj, i)):
        funcs[getattr(obj, i).__name__] = getattr(obj, i)
print(funcs)
print("等待请求")

port = "5555"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)

# time.sleep(5)
while True:
    socket.send_json({"token": "1234567890", "function": "station_total_generation", "args": [10, 10]})
    msg = socket.recv_json()
    print(msg)
# func = msg["function"]
# token = msg["token"]
# args = msg["args"]
#
# result = funcs[func](*args)
# socket.send_json({"token": token, "result": result})
