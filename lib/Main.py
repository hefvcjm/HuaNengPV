# coding = utf-8
from lib.execute.service import ZmqService

if __name__ == '__main__':
    ZmqService(url="tcp://*:5571", role="server").start()
    ZmqService(url="tcp://localhost:5555", role="client").start()
