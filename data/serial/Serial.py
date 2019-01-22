# coding = utf-8
from data.model.Config import *
from data.model.Input import *
from data.model.Output import *


class Serial(Model.Model):
    class SerialConfig(Config):

        def __init__(self):
            super().__init__()
            self.N = 0  # 组串个数

    class SerialInput(Input):

        def __init__(self):
            super().__init__()
            self.modules = []  # 组件

    class SerialOutput(Output):

        def __init__(self):
            super().__init__()
            self.I = 0  # 输出电流
            self.V = 0  # 输出电压

    def __init__(self, m_input=None, m_output=None, m_config=None):
        super().__init__(m_input, m_output, m_config)

        if m_input is None:
            self.input = self.SerialInput()

        if m_output is None:
            self.output = self.SerialOutput()

        if m_config is None:
            self.config = self.SerialConfig()

        self.loss = 0
        self.T = 0

    def calc_output(self):
        super().calc_output()
        if len(self.input.modules) == 0:
            self.output.I = 0
            self.output.V = 0
            return
        self.output.I = max([item.output.I for item in self.input.modules])
        self.output.V = sum([item.output.V for item in self.input.modules])
