# coding = utf-8
import os
import sys

sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], ".."))

from lib.execute.service import ZmqService

if __name__ == '__main__':
    ZmqService(url="tcp://*:5571", role="server").start()
    ZmqService(url="tcp://localhost:5555", role="client").start()
