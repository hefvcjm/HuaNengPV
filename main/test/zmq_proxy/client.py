import zmq
import random
from threading import Thread
import time
import numpy as np


def test_serial_current_zero(socket):
    count = 0
    #  发送问题给ROUTER
    for request in range(1, 11):
        socket.send_json({'target': 'require algorithm', 'function': '故障诊断', 'detail': {'type': '某一支路电流为零'}})
        message = socket.recv()
        print("1 Received reply %s [%s]" % (request, message.decode('unicode_escape')))
        socket.send_json(
            {'target': 'set data', 'function': '故障诊断', 'data': {'current': random.uniform(0, 0.015), 'count': count}})
        message = socket.recv()
        print("1 Received reply %s [%s]" % (request, message.decode('unicode_escape')))
        print(message.decode())
        count = eval(message.decode())['count']


def test_serial_current_low(socket):
    #  发送问题给ROUTER
    for request in range(1, 11):
        socket.send_json({'target': 'require algorithm', 'function': '故障诊断', 'detail': {'type': '支路电流偏低'}})
        message = socket.recv()
        print("2 Received reply %s [%s]" % (request, message.decode('unicode_escape')))
        socket.send_json({'target': 'set data', 'function': '故障诊断', 'data': {'current': random.uniform(0, 0.015)}})
        message = socket.recv()
        print("2 Received reply %s [%s]" % (request, message.decode('unicode_escape')))
        print(message.decode())


def rate(x):
    random = np.random.normal(0, 0.1, 1)[0]
    # print(random)
    return -0.012 * x + 18 + random


def test_prediction_conversion(socket):
    x = [round(rate(x), 2) for x in range(300)]
    history = x[:100]
    socket.send_json({'target': 'require algorithm', 'function': '寿命评估', 'detail': {'type': '预测组串光电转化率'}})
    message = socket.recv()
    print("2 Received reply %s [%s]" % ('conversion', message.decode('unicode_escape')))
    socket.send_json({'target': 'set data', 'function': '寿命评估', 'data': {'conversion': history}})
    message = socket.recv()
    print("2 Received reply %s [%s]" % ('conversion', message.decode('unicode_escape')))
    print(message.decode())


# Prepare our context and sockets
context = zmq.Context()
socket1 = context.socket(zmq.REQ)
socket1.identity = b'A'
# socket1.setsockopt(zmq.IDENTITY, b'A')
# 这一次，我们不连接REP，而是连接ROUTER，多个REP连接一个ROUTER
socket1.connect("tcp://localhost:5570")
socket2 = context.socket(zmq.REQ)
socket2.identity = b'B'
# socket2.setsockopt(zmq.IDENTITY, b'B')
# 这一次，我们不连接REP，而是连接ROUTER，多个REP连接一个ROUTER
socket2.connect("tcp://localhost:5570")
socket3 = context.socket(zmq.REQ)
socket3.identity = b'C'
# socket2.setsockopt(zmq.IDENTITY, b'B')
# 这一次，我们不连接REP，而是连接ROUTER，多个REP连接一个ROUTER
socket3.connect("tcp://localhost:5570")
Thread(target=test_serial_current_zero, args=(socket1,)).start()
# time.sleep(2)
Thread(target=test_serial_current_low, args=(socket2,)).start()
Thread(target=test_prediction_conversion, args=(socket3,)).start()
# socket.close()
# context.term()
