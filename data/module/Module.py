# coding = utf-8
# 光伏组件
from ..model import *


class Module(Model.Model):

    def __init__(self, m_input=None, m_output=None, m_loss=None, m_config=None):
        super().__init__(m_input, m_output, m_loss, m_config)
        if m_config is None:
            self.config.params["I"] = 0
            self.config.params["V"] = 0
            self.config.params["G"] = 0
            self.config.params["T"] = 0
            self.config.params["S"] = 0
            self.config.params["rate"] = 0

        if m_input is None:
            self.input.params["G"] = 0
            self.input.params["T"] = 0

        if m_output is None:
            self.output.params["I"] = 0
            self.output.params["V"] = 0
            self.output.params["P"] = 0

        if m_loss is None:
            self.loss.params["p_loss"] = 0
