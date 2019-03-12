# coding = utf-8
# 光伏组件
import json
from SimulationPV.module.DetailedConfig import *
from SimulationPV.module.Calculate import *


# default_type = {
#     "Uoc_ref": 36.3,
#     "Isc_ref": 7.84,
#     "Rsh_ref": 313.3991,
#     "Rs_ref": 0.39383,
#     "Tref": 298.15,
#     "Sref": 1000,
#     "Alpha": 0.102,
#     "Beta": -0.36099,
#     "Ns": 60,
#     "n": 0.98117,
# }

class Module:

    def __init__(self, config=default_type):
        self.config = config
        self.T = None
        self.G = None
        self.Pmax = None
        self.Umax = None
        self.Imax = None

    def set_config(self, config):
        self.config = config

    def set_input(self, T, G):
        self.T = T
        self.G = G

    def calc_output(self):
        Iph = get_iph(self.config["Isc_ref"], self.config["Alpha"], self.config["Tref"], self.config["Sref"], self.T,
                      self.G)
        Io = get_io(self.config["Isc_ref"], self.config["Uoc_ref"], self.config["Alpha"], self.config["Beta"],
                    self.config["Tref"], self.config["n"], self.T)
        Rsh = get_rsh(self.config["Rsh_ref"], self.config["Sref"], self.G)
        self.Pmax, self.Umax, self.Imax = get_max_power_point(Iph, Io, self.config["n"], Rsh, self.config["Rs_ref"],
                                                              self.T)
        return self.Umax, self.Imax

    def get_measure(self):
        return {
            "T": self.T,
            "G": self.G,
            "Pmax": self.Pmax,
            "Umax": self.Umax,
            "Imax": self.Imax
        }

    def format_object(self):
        return {
            "config": self.config,
            "T": self.T,
            "G": self.G,
            "Pmax": self.Pmax,
            "Umax": self.Umax,
            "Imax": self.Imax
        }


# module = Module()
# module.set_input(300, 1243)
# module.calc_output()
# print(json.dumps(module.format_object(), indent=4))
