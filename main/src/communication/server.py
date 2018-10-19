# -*- coding: UTF-8 -*-
import zmq
import threading
import json
from main.src.communication.FunctionMapping import *

# client id --> 处理类实例
ID_CLASS_MAPPING = {}
# 开启服务器线程数量
server_thread_count = 5


class ServerTask(threading.Thread):
    """ServerTask"""

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind('tcp://*:5570')

        backend = context.socket(zmq.DEALER)
        backend.bind('inproc://backend')

        workers = []
        for i in range(server_thread_count):
            worker = ServerWorker(context)
            worker.start()
            workers.append(worker)

        zmq.proxy(frontend, backend)

        frontend.close()
        backend.close()
        context.term()


class ServerWorker(threading.Thread):
    """ServerWorker"""

    def __init__(self, context):
        threading.Thread.__init__(self)
        self.context = context

    def run(self):
        worker = self.context.socket(zmq.DEALER)
        worker.connect('inproc://backend')
        print('Worker started')
        while True:
            ident, empty, message = worker.recv_multipart()
            print("server received: %s" % message.decode('unicode_escape'))
            try:
                json_msg = json.loads(message.decode())
                if 'target' in json_msg.keys() and 'function' in json_msg.keys():
                    if json_msg['target'] == 'require algorithm':
                        path = None
                        if json_msg['function'] == '故障诊断':
                            if 'detail' in json_msg.keys():
                                path = DIAGNOSIS_FUNCTION_MAPPING[json_msg['detail']['type']]
                        elif json_msg['function'] == '寿命评估':
                            if 'detail' in json_msg.keys():
                                path = PREDICTION_FUNCTION_MAPPING[json_msg['detail']['type']]
                        print(path)
                        if path is not None:
                            obj = __import__(path, fromlist=path.split('.')[:-1])
                            clazz = getattr(obj, 'Application')
                            instance = clazz(ident, worker)
                            ID_CLASS_MAPPING[ident] = instance
                        else:
                            worker.send(
                                [ident, empty,
                                 json.dumps({'error': '不存在该算法功能：' + json_msg['function']}).encode()])
                    elif json_msg['target'] == 'set data':
                        data = None
                        if json_msg['function'] == '故障诊断':
                            if 'data' in json_msg.keys():
                                data = json_msg['data']
                        elif json_msg['function'] == '寿命评估':
                            if 'data' in json_msg.keys():
                                data = json_msg['data']
                        if not isinstance(data, dict):
                            worker.send([ident, empty, json.dumps({'error': '数据格式错误'}).encode()])
                            continue
                        instance = ID_CLASS_MAPPING[ident]
                        if instance is not None:
                            method = getattr(instance, 'main')
                            method(data)
                        else:
                            worker.send([ident, empty, json.dumps({'error': '未初始化算法'}).encode()])
            except json.JSONDecodeError:
                worker.send([ident, empty, json.dumps({'error': 'json解析错误'}).encode()])
        worker.close()


def init():
    # 初始化故障诊断模块
    base_diagnosis_path = 'main.src.use.diagnosis'
    obj = __import__(base_diagnosis_path, fromlist=base_diagnosis_path.split('.'))
    all_modules = getattr(obj, '__all__')
    print("初始化故障诊断模块映射字典：")
    for module in all_modules:
        module_name = base_diagnosis_path + '.' + module
        module_obj = __import__(module_name, fromlist=module_name.split('.')[:-1])
        fault_name = getattr(module_obj, 'fault_name')
        DIAGNOSIS_FUNCTION_MAPPING[fault_name] = module_name
        print('映射:' + fault_name + '-->' + module_name)
    print('共' + str(len(all_modules)) + '个故障诊断模块')
    # 初始化寿命预测模块
    base_diagnosis_path = 'main.src.use.prediction'
    obj = __import__(base_diagnosis_path, fromlist=base_diagnosis_path.split('.'))
    all_modules = getattr(obj, '__all__')
    print("初始化寿命评估模块映射字典：")
    for module in all_modules:
        module_name = base_diagnosis_path + '.' + module
        module_obj = __import__(module_name, fromlist=module_name.split('.')[:-1])
        fault_name = getattr(module_obj, 'func_name')
        PREDICTION_FUNCTION_MAPPING[fault_name] = module_name
        print('映射:' + fault_name + '-->' + module_name)
    print('共' + str(len(all_modules)) + '个寿命评估模块')
    print('初始化完成')


def main():
    """main function"""
    init()
    server = ServerTask()
    server.start()
    server.join()


if __name__ == "__main__":
    main()
