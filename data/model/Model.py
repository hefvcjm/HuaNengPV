# coding=utf-8
import re

from data.model.Config import Config
from data.model.Port import Port


class Model:

    def __init__(self, m_input=None, m_output=None, m_config=None):
        self.input = m_input
        self.output = m_output
        self.config = m_config

    def set_config(self, config):
        self.config = config

    def set_input(self, stream):
        self.input = stream

    def set_output(self, stream):
        self.output = stream

    def calc_loss(self):
        pass

    def calc_output(self):
        pass

    def format_object(self):
        result = dict()
        for item in dir(self):
            if not re.match("^_.*", item):
                attr = getattr(self, item)
                if not callable(attr):
                    if isinstance(attr, Config) or isinstance(attr, Port):
                        result[item] = attr.format_object()
                    else:
                        result[item] = attr
        return result
