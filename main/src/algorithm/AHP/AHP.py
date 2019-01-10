# coding = utf-8
# 实现层次分析法进行综合评价
from functools import reduce

import numpy as np
from main.src.log.Log import *
from main.src.algorithm.AHP.config import *


class AHP:
    class Node:
        """
        定义层次分析法中的节点
        """

        def __init__(self, **kwargs):
            """
            构造函数
            :param kwargs: 初始化节点参数，score: 分数; sub_nodes: 子节点, jd_mat: 判断矩阵
            """
            self.score = kwargs["score"] if "score" in kwargs.keys() else None
            self.__sub_nodes = kwargs["sub_nodes"] if "sub_nodes" in kwargs.keys() else None
            self.__judgement_matrix = kwargs["jd_mat"] if "jd_mat" in kwargs.keys() else None
            self.__n = None  # 阶数
            self.__max_characteristic_value = None  # 最大特征值
            self.__weight_vector = None  # 权值向量
            self.__consistence = None  # 一致性
            if self.score is not None:
                if not isinstance(self.score, float) and not isinstance(self.score, int):
                    raise Exception("非法参数类型", kwargs["score"])
            if self.__sub_nodes is not None:
                if not isinstance(self.__sub_nodes, list) and not isinstance(self.__sub_nodes, np.ndarray):
                    raise Exception("非法参数类型", kwargs["sub_nodes"])
                if len(list(self.__sub_nodes)) == 0 or not isinstance(self.__sub_nodes[0], type(self)):
                    raise Exception("非法参数类型", kwargs["sub_nodes"])
            if self.__judgement_matrix is not None:
                if not isinstance(self.__judgement_matrix, list) \
                        and not isinstance(self.__judgement_matrix, np.ndarray):
                    raise Exception("非法参数类型", kwargs["sub_nodes"])
                self.__judgement_matrix = np.array(self.__judgement_matrix, float)
                self.__norm_jd_mat()
                self.__jd_mat_max_characteristic_value()
                self.__calc_weight_vector()
                self.__consistence_check()
            if not self.__consistence:
                raise Exception("判断矩阵不通过一致性检测")

        def __norm_jd_mat(self):
            """
            归一化判断矩阵
            :return:
            """
            logger.debug(self.__judgement_matrix)
            x, y = self.__judgement_matrix.shape
            for i in range(y):
                self.__judgement_matrix[:, i] = self.__judgement_matrix[:, i] / sum(self.__judgement_matrix[:, i])
            logger.debug(self.__judgement_matrix)

        def __jd_mat_max_characteristic_value(self):
            """
            计算判断矩阵最大特征值和对应的特征向量
            :return: 最大特征值和对应的特征向量
            """
            v, w = np.linalg.eig(self.__judgement_matrix)
            self.__n = len(v)
            self.__max_characteristic_value = max(v)

        def __calc_weight_vector(self):
            """
            计算权值向量
            :return:
            """
            temp = []
            x, y = self.__judgement_matrix.shape
            for i in range(x):
                row = self.__judgement_matrix[i, :]
                temp.append(reduce(lambda x, y: x * y, row) ** (1. / (y * 1.)))
            logger.debug(temp)
            self.__weight_vector = temp

        def __consistence_check(self):
            """
            一致性检测
            :return:
            """
            if self.__n <= 2:
                self.__consistence = True
                return
            if self.__max_characteristic_value / RI[self.__n] < 0.1:
                self.__consistence = True
            else:
                self.__consistence = False

        def to_string(self):
            """
            格式化对象为字符串
            :return:
            """
            string = "\n\t节点: {},\n" \
                     "\t阶数: {},\n" \
                     "\t最大特征值: {},\n" \
                     "\t权值向量: {},\n" \
                     "\t一致性: {}\n"
            string = string.format(self, self.__n, self.__max_characteristic_value, self.__weight_vector,
                                   self.__consistence)
            return string

        def get_weight(self):
            """
            获取节点的权值向量
            :return: 权值向量
            """
            return self.__weight_vector


jd_mat = [[1., 3.], [1. / 3., 1.]]
node = AHP.Node(jd_mat=jd_mat)
logger.debug(node.to_string())
