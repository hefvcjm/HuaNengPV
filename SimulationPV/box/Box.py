# coding = utf-8
# 汇流箱
from SimulationPV.serial.Serial import *


class Box:

    def __init__(self):
        self.input = []
        self.I = None
        self.U = None
        self.lu = 0
        self.li = 0

    def set_input(self, serial_list):
        self.input = serial_list

    def add_input(self, serial):
        self.input.append(serial)

    def set_loss(self, lu, li):
        self.lu = lu
        self.li = li

    def calc_output(self):
        if len(self.input) == 0:
            self.I = 0
            self.U = 0
            return self.I, self.U
        self.I = sum([module.I for module in self.input]) * (1 - self.li)
        self.U = min([module.U for module in self.input]) * (1 - self.lu)
        return self.U, self.I

    def get_measure(self):
        return {
            "U": self.U,
            "I": self.I
        }

    def format_object(self):
        return {
            "input": [serial.format_object() for serial in self.input],
            "U": self.U,
            "I": self.I
        }


module = Module()
module.set_input(300, 1243)
serial = Serial()
module.calc_output()
serial.set_input([module] * 10)
serial.calc_output()
box = Box()
box.set_input([serial] * 10)
box.calc_output()
print(json.dumps(box.format_object(), indent=4))
