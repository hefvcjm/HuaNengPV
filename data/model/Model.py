# coding=utf-8
import json


class Model:

    def __init__(self, m_input=None, m_output=None, m_loss=None, m_config=None):
        self.input = m_input
        self.output = m_output
        self.loss = m_loss
        self.config = m_config

    def set_config(self, config):
        self.config = config

    def set_input(self, stream):
        self.input = stream

    def set_output(self, stream):
        self.output = stream

    def set_loss(self, loss):
        self.loss = loss

    def calc_loss(self):
        pass

    def calc_output(self):
        pass
