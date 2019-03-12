# coding = utf-8
# 组串
from SimulationPV.module.Module import *


class Serial:

    def __init__(self):
        self.input = []
        self.I = None
        self.U = None
        self.lu = 0
        self.li = 0

    def set_input(self, module_list):
        self.input = module_list

    def add_input(self, module):
        self.input.append(module)

    def set_loss(self, lu, li):
        self.lu = lu
        self.li = li

    def calc_output(self):
        if len(self.input) == 0:
            self.I = 0
            self.U = 0
            return self.I, self.U
        self.I = min([module.Imax for module in self.input]) * (1 - self.li)
        self.U = sum([module.Umax for module in self.input]) * (1 - self.lu)
        return self.U, self.I

    def get_measure(self):
        return {
            "U": self.U,
            "I": self.I
        }

    def format_object(self):
        return {
            "input": [module.format_object() for module in self.input],
            "U": self.U,
            "I": self.I
        }


# module = Module()
# module.set_input(300, 1243)
# serial = Serial()
# module.calc_output()
# serial.set_input([module] * 10)
# serial.calc_output()
# print(json.dumps(serial.format_object(), indent=4))
