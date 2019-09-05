# coding = utf-8
import zmq
import threading
from lib.thread.ThreadPool import ThreadPool
from functools import partial
from lib.logger import log
from lib.execute.exec import execute


class ZmqService(threading.Thread):

    def __init__(self, url: str, role: str = "server", max_workers: int = 5):
        threading.Thread.__init__(self)
        self.__url = url
        self.__role = role.lower()
        self.__max_workers = max_workers
        self.__worker_queue = set()
        if role.lower() not in ["server", "client"]:
            log.warn("没有相应的角色选择[role=%s]，将设置为默认项[role=%s]，可选项包括：%s" % (self.__role, "server", ["server", "client"]))
            self.__role = "server"  # default
        self.__socket = None

    def __send_json(self, data):
        self.__socket.send_json(data)
        log.info(f"send: {data}")

    def __remove_token(self, token):
        try:
            self.__worker_queue.remove(token)
        except Exception as e:
            log.error(f"删除{token}出错:{e}")

    def run(self):
        self.__socket = zmq.Context().socket(zmq.PAIR)
        try:
            if self.__role == "server":
                self.__socket.bind(self.__url)
            else:
                self.__socket.connect(self.__url)
        except Exception as e:
            log.error("ZMQ连接参数错误，信息：%s" % e)
            return
        executor = ThreadPool(max_pool=5, queue_size=10 ** 8)
        log.info("Worker开启，服务角色为【%s】，创建最大线程数为【%s】的线程池处理请求" % (self.__role, self.__max_workers))
        log.info("等待请求 ...")
        while True:
            try:
                try:
                    msg = self.__socket.recv_json()
                except Exception as e:
                    self.__send_json({"token": None, "result": None, "err": "数据接收出错"})
                    continue
                log.info("接收到消息: %s" % msg)
                try:
                    assert msg.get("token") is not None
                    assert msg.get("function") is not None
                    assert msg.get("args") is not None
                except AssertionError as e:
                    self.__send_json({"token": msg.get("token"), "result": None, "err": "json格式出错，无法完成解析"})
                    continue
                if msg["token"] in self.__worker_queue:
                    self.__send_json(
                        {"token": msg["token"], "result": None, "err": "token=%s对应的请求正在执行" % msg["token"]})
                    continue
                else:
                    self.__worker_queue.add(msg["token"])
                try:
                    executor.submit(fn=execute, callback=partial(self.done, token=msg["token"]), timeout=5, **msg)
                except Exception as e:
                    self.__send_json(
                        {"token": msg["token"], "result": None, "err": "提交请求出错"})
                    self.__remove_token(msg["token"])
                    continue
            except Exception as exce:
                log.error(f"错误信息:{exce}")

    def done(self, result, token):
        log.info(f"send: {result}")
        self.__socket.send_json(result)
        self.__remove_token(token)

    @property
    def socket(self):
        return self.__socket

    @property
    def role(self):
        return self.__role

# ZmqService(url="tcp://*:5571", role="server").start()
# ZmqService(url="tcp://localhost:5555", role="client").start()
