# coding = utf-8
from data.model import *


class Box(Model.Model):
    class BoxConfig(Config.Config):

        def __init__(self):
            super().__init__()
            self.V_max = 0  # 最大输入电压
            self.V_min = 0  # 最小输入电压
            self.I_max = 0  # 最大输入电流
            self.N = 0  # 并联组串数
            self.I_out_max = 0  # 最大输出电流

    class BoxInput(Input.Input):

        def __init__(self):
            super().__init__()
            self.serials = []  # 组串

    class BoxOutput(Output.Output):

        def __init__(self):
            super().__init__()
            self.I = 0  # 输出电流
            self.V = 0  # 输出电压

    def __init__(self, m_input=None, m_output=None, m_config=None):
        super().__init__(m_input, m_output, m_config)
        if m_config is None:
            self.config = self.BoxConfig()

        if m_input is None:
            self.input = self.BoxInput()

        if m_output is None:
            self.output = self.BoxOutput()

        self.loss = 0
        self.T = 0

    def calc_output(self):
        super().calc_output()
        if len(self.input.serials) == 0:
            self.output.I = 0
            self.output.V = 0
            return
        self.output.I = sum([item.I for item in self.input.serials])
        self.output.V = max([item.V for item in self.input.serials])
