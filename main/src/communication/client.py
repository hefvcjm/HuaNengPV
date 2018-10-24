# -*- coding: UTF-8 -*-
import zmq
import json
import threading
from main.src.communication.FunctionMapping import *

# client id --> 处理类实例
ID_CLASS_MAPPING = {}
# 开启服务器线程数量
server_thread_count = 5


class Client(threading.Thread):
    __socket = None
    __context = None
    __url = None

    def __init__(self, url):
        threading.Thread.__init__(self)
        self.__context = zmq.Context()
        self.__url = url
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
        FUNCTION_MAPPING.update(DIAGNOSIS_FUNCTION_MAPPING)
        FUNCTION_MAPPING.update(PREDICTION_FUNCTION_MAPPING)
        print('初始化完成')

    def run(self):
        self.__socket = self.__context.socket(zmq.PAIR)
        self.__socket.connect(self.__url)
        print('Worker started')
        while True:
            message = self.__socket.recv()
            message = message.decode('utf-8')
            print("server received: %s" % message)
            token = None
            try:
                json_msg = json.loads(message)
                print(json_msg.keys())
                if 'token' in json_msg.keys():
                    token = json_msg['token']
                else:
                    self.__socket.send_json({'type': 'error', 'token': token, 'data': {'msg': '未设置token'}})
                    continue
                if json_msg['type'] == 'trigger':
                    path = FUNCTION_MAPPING[json_msg['detail']['type']]
                    print(path)
                    if path is not None:
                        obj = __import__(path, fromlist=path.split('.')[:-1])
                        clazz = getattr(obj, 'Application')
                        instance = clazz(token, self.__socket)
                        ID_CLASS_MAPPING[token] = instance
                    else:
                        self.__socket.send_json(
                            {'type': 'error', 'token': token, 'data': {'msg': '不存在该算法功能：' + json_msg['function']}})
                        continue
                elif json_msg['type'] == 'response':
                    data = json_msg['device']
                    if not isinstance(data, list):
                        self.__socket.send_json({'type': 'error', 'token': token, 'data': {'msg': '数据格式错误'}})
                        continue
                    instance = ID_CLASS_MAPPING[token]
                    if instance is not None:
                        method = getattr(instance, 'main')
                        method(data)
                    else:
                        self.__socket.send_json({'type': 'error', 'token': token, 'data': {'msg': '未初始化算法'}})
                else:
                    self.__socket.send_json(
                        {'type': 'error', 'token': token, 'data': {'msg': '无相关的命令：' + json_msg['type']}})
            except json.JSONDecodeError:
                self.__socket.send_json({'type': 'error', 'token': token, 'data': {'msg': 'json解析错误'}})
            except KeyError:
                self.__socket.send_json({'type': 'error', 'token': token, 'data': {'msg': 'json键出错'}})
            except:
                pass
        self.__socket.close()


def main():
    """main function"""
    client = Client('tcp://localhost:3000')
    client.start()
    client.join()


if __name__ == "__main__":
    main()
