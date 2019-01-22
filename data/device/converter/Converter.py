# coding = utf-8
from data.model import *


class Converter(Model.Model):
    class ConverterConfig(Config.Config):

        def __init__(self):
            super().__init__()
            self.P_in_max = 0  # 最大输入功率
            self.V_in_max = 0  # 最大输入电压
            self.V_boot = 0  # 启动电压
            self.V_in = 0  # 额定输入电压
            self.I_in_max = 0  # 最大输入电流
            self.P_out = 0  # 额定输出功率
            self.P_var = 0  # 额定视在功率
            self.V_out = 0  # 额定输出电压
            self.F_out = 0  # 额定输出频率
            self.I_out = 0  # 额定输出电流
            self.fi = 0  # 功率因数
            self.efficiency = 0  # 效率

    class ConverterInput(Input.Input):

        def __init__(self):
            super().__init__()
            self.boxes = []  # 汇流箱

    class ConverterOutput(Output.Output):

        def __init__(self):
            super().__init__()
            self.I = 0  # 输出电流
            self.V = 0  # 输出电压
            self.F = 0  # 输出频率
            self.fi = 0  # 功率因数

    def __init__(self, m_input=None, m_output=None, m_config=None):
        super().__init__(m_input, m_output, m_config)

        if m_config is None:
            self.config = self.ConverterConfig()

        if m_input is None:
            self.input = self.ConverterInput()

        if m_output is None:
            self.ConverterOutput = self.ConverterOutput()

        self.loss = 0
        self.T = 0
