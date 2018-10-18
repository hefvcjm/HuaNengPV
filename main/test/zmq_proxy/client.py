import zmq
import random
from threading import Thread
import time


def test_serial_current_zero(socket):
    count = 0
    #  发送问题给ROUTER
    for request in range(1, 11):
        socket.send_json({'target': 'require algorithm', 'function': '某一支路电流为零'})
        message = socket.recv()
        print("1 Received reply %s [%s]" % (request, message.decode()))
        socket.send_json({'current': random.uniform(0, 0.015), 'count': count})
        message = socket.recv()
        print("1 Received reply %s [%s]" % (request, message.decode()))
        print(message.decode())
        count = eval(message.decode())['count']


def test_serial_current_low(socket):
    #  发送问题给ROUTER
    for request in range(1, 11):
        socket.send_json({'target': 'require algorithm', 'function': '支路电流偏低'})
        message = socket.recv()
        print("2 Received reply %s [%s]" % (request, message.decode()))
        socket.send_json({'current': random.uniform(0, 0.015)})
        message = socket.recv()
        print("2 Received reply %s [%s]" % (request, message.decode()))
        print(message.decode())


# Prepare our context and sockets
context1 = zmq.Context()
socket1 = context1.socket(zmq.REQ)
socket1.setsockopt(zmq.IDENTITY, b'A')
# 这一次，我们不连接REP，而是连接ROUTER，多个REP连接一个ROUTER
socket1.connect("tcp://localhost:5559")
context2 = zmq.Context()
socket2 = context2.socket(zmq.REQ)
socket2.setsockopt(zmq.IDENTITY, b'B')
# 这一次，我们不连接REP，而是连接ROUTER，多个REP连接一个ROUTER
socket2.connect("tcp://localhost:5559")
Thread(target=test_serial_current_zero, args=(socket1,)).start()
# time.sleep(2)
Thread(target=test_serial_current_low, args=(socket2,)).start()
# socket.close()
# context.term()
