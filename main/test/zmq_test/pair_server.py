# coding = utf-8

import zmq
import random
import sys
import time

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
print(socket.bind)
socket.bind("tcp://*:%s" % port)

while True:
    socket.send_json({"a": 1, "b": 1})
    msg = socket.recv()
    print(msg)
    time.sleep(1)
