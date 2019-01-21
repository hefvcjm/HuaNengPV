# coding = utf-8
# 光伏组件
from ..model import *


class Module(Model.Model):
    class ModuleConfig(Config.Config):

        def __init__(self):
            super().__init__()
            self.Pn = 0  # 最大功率
            self.Vn = 0  # 最大功率点电压
            self.In = 0  # 最大功率点电流
            self.Voc = 0  # 开路电压
            self.Isc = 0  # 短路电流
            self.efficiency = 0  # 组件效率
            self.S = 0  # 组件面积

    class ModuleInput(Input.Input):

        def __init__(self):
            super().__init__()
            self.G = 0  # 辐照度
            self.Te = 0  # 环境温度
            self.Tm = 0  # 组件温度

    class ModuleOutput(Output.Output):

        def __init__(self):
            super().__init__()
            self.I = 0  # 输出电流
            self.V = 0  # 输出电压

    def __init__(self, m_input=None, m_output=None, m_config=None):
        super().__init__(m_input, m_output, m_config)
        if m_config is None:
            self.config = self.ModuleConfig()

        if m_input is None:
            self.input = self.ModuleInput()

        if m_output is None:
            self.output = self.ModuleOutput()

        self.loss = 0  # 损耗
