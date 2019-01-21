# coding = utf-8
from ..model import *


class Box(Model.Model):

    def __init__(self, m_input=None, m_output=None, m_loss=None, m_config=None):
        super().__init__(m_input, m_output, m_loss, m_config)
        if m_config is None:
            self.config.params["I"] = 0
            self.config.params["V"] = 0
            self.config.params["T"] = 0

        if m_input is None:
            self.input.params["serial"] = []
            self.input.params["count"] = len(self.input.params["serial"])

        if m_output is None:
            self.output.params["I"] = 0
            self.output.params["V"] = 0
            self.output.params["P"] = 0

        if m_loss is None:
            self.loss.params["p_loss"] = 0

    def calc_output(self):
        if self.input.params["count"] == 0:
            self.output.params["I"] = 0
            self.output.params["V"] = 0
            self.output.params["P"] = 0
            return
        self.output.params["I"] = sum([item.output.params["I"] for item in self.input.params["serial"]])
        self.output.params["V"] = max([item.output.params["V"] for item in self.input.params["serial"]])
        self.output.params["P"] = self.output.params["I"] * self.output.params["V"]
