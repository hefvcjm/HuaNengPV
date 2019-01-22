# coding = utf-8
import re

from data.model import Model


class Port:

    def __init__(self):
        pass

    def format_object(self):
        result = dict()
        for item in dir(self):
            if not re.match("^_.*", item):
                attr = getattr(self, item)
                if not callable(attr):
                    if isinstance(attr, list) and len(attr) != 0 and isinstance(attr[0], Model.Model):
                        result[item] = [i.format_object() for i in attr]
                    else:
                        result[item] = attr
        return result
