# coding = utf-8
import copy
from . import *


def execute(token: str, function: str, args: list) -> dict:
    func = FUNCTION_MAP.get(function)
    if func is None:
        err = "找不到功能模块：%s" % function
        return {"token": token, "result": None, "err": err}
    try:
        result = func(*args)
        return {"token": token, "result": result, "err": None}
    except Exception as e:
        err = "功能模块[%s]运行出错：%s" % (function, e)
        return {"token": token, "result": None, "err": err}


def response(socket, **kwargs):
    temp_socket = copy.deepcopy(socket)
    result = execute(**kwargs)
    temp_socket.send_json(result)
    return result
