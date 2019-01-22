# coding = utf-8
from data.module.Module import *
from data.serial.Serial import *
from data.box.Box import *
from data.converter.Converter import *
import time
import json

# 设置光伏电站结构
converters = []
# 20台逆变器
for i in range(10):
    converter = Converter()
    # 每台逆变器配备6台汇流箱
    for j in range(4):
        box = Box()
        # 每台汇流箱连接16路组串
        for k in range(8):
            serial = Serial()
            for n in range(6):
                module = Module(None, None)
                serial.input.modules.append(module)
            box.input.serials.append(serial)
        converter.input.boxes.append(box)
    converters.append(converter)

while True:
    for converter in converters:
        for box in converter.input.boxes:
            for serial in box.input.serials:
                for module in serial.input.modules:
                    module.calc_output()
                serial.calc_output()
            box.calc_output()
        converter.calc_output()
        print(json.dumps(converter.format_object(), indent=4))
    time.sleep(10)
