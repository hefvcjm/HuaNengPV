# coding = utf-8
import json
import re


class Port:

    def __init__(self):
        pass

    def format_object(self):
        result = dict()
        for item in dir(self):
            if not re.match("^_.*", item):
                attr = getattr(self, item)
                if not callable(attr):
                    result[item] = attr
        return result
