# coding = utf-8
import logging
import inspect
from lib.logger import log

FUNCTION_MAP = {}

__FUNCTION_MODULE_PATH = ["lib.algorithm.func.calculate", "lib.algorithm.func.detection", "lib.algorithm.func.health",
                          "lib.algorithm.func.iip", "lib.algorithm.func.life_predict"]


def __mapping():
    total = 0
    for module_path in __FUNCTION_MODULE_PATH:
        obj = __import__(module_path, fromlist=module_path.split('.'))
        # print(dir(obj))
        count = 0
        for i in dir(obj):
            if callable(getattr(obj, i)) and (
                    not inspect.isbuiltin(getattr(obj, i)) and inspect.isroutine(getattr(obj, i))):
                if FUNCTION_MAP.get(getattr(obj, i).__name__) is None:
                    count += 1
                FUNCTION_MAP[getattr(obj, i).__name__] = getattr(obj, i)
        log.info("在%s中共找到%s个功能函数。" % (module_path, count))
        total += count
    log.info("完成查找映射，找到%s个功能函数。" % total)


__mapping()
