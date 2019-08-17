# coding = utf-8
import zmq
import random
import sys
import time

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:%s" % port)

while True:
    # msg = socket.recv()
    msg = socket.recv_json()
    print(msg)
    socket.send_json({"a": 2, "b": 2})
    socket.send_json({"a": 3, "b": 3})
    time.sleep(1)
