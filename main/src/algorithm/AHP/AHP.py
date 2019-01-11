# coding = utf-8
# 实现层次分析法进行综合评价
from functools import reduce

import numpy as np
from main.src.log.Log import *
from main.src.algorithm.AHP.config import *
import copy


class AHP:
    class Node:
        """
        定义层次分析法中的节点
        """

        def __init__(self, **kwargs):
            """
            构造函数
            :param kwargs: 初始化节点参数，score: 分数; sub_nodes: 子节点, jd_mat: 判断矩阵; name: 节点名称
            """
            self.score = kwargs["score"] if "score" in kwargs.keys() else None
            self.__sub_nodes = copy.deepcopy(kwargs["sub_nodes"]) if "sub_nodes" in kwargs.keys() else None
            self.__judgement_matrix = copy.deepcopy(kwargs["jd_mat"]) if "jd_mat" in kwargs.keys() else None
            self.__name = kwargs["name"] if "name" in kwargs.keys() else None
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
                if self.__sub_nodes is not None:
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
            logger.debug("\n{}".format(self.__judgement_matrix))
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
            self.__weight_vector = np.array(temp)

        def __consistence_check(self):
            """
            一致性检测
            :return:
            """
            if self.__n <= 2:
                self.__consistence = True
                return
            if ((self.__max_characteristic_value - self.__n) / (self.__n - 1)) / RI[self.__n] < 0.1:
                self.__consistence = True
            else:
                self.__consistence = False

        def to_string(self):
            """
            格式化对象为字符串
            :return:
            """
            string = "\n\t节点: {},\n" \
                     "\t名称: {},\n" \
                     "\t阶数: {},\n" \
                     "\t最大特征值: {},\n" \
                     "\t权值向量: {},\n" \
                     "\t一致性: {},\n" \
                     "\t评分: {}\n"
            string = string.format(self, self.__name, self.__n, self.__max_characteristic_value, self.__weight_vector,
                                   self.__consistence, self.score)
            return string

        def get_weight(self):
            """
            获取节点的权值向量
            :return: 权值向量
            """
            return self.__weight_vector

        def get_name(self):
            """
            获取节点名称
            :return: 节点名称
            """
            return self.__name

        def get_sub_nodes(self):
            """
            获取子节点
            :return: 子节点
            """
            return self.__sub_nodes

    def __init__(self, root_node, is_copy=True):
        if is_copy:
            self.root_node = copy.deepcopy(root_node)
        else:
            self.root_node = root_node

    def evaluate(self, adaptive_weight=False):
        """
        计算根节点得分
        :param adaptive_weight 是否变权
        :return: 根节点得分
        """
        balance_func = None
        if adaptive_weight:
            def __balance_func(node):
                temp = []
                for i in zip(node.get_weight(), node.get_sub_nodes()):
                    score = __get_score(i[1])
                    if score < 10:
                        score = 10
                    temp.append(i[0] * (score ** (a - 1)))
                sum_temp = sum(temp)
                return np.array([i / sum_temp for i in temp])

            balance_func = __balance_func
        else:
            balance_func = lambda x: x.get_weight()

        def __get_score(node):
            """
            计算某个节点和递归到叶节点的得分
            :param node: 节点
            :return: 节点得分
            """
            sub_nodes = node.get_sub_nodes()
            if sub_nodes is None:
                return node.score
            elif node.score is not None:
                return node.score
            else:
                node.score = balance_func(node).dot(np.array([__get_score(item) for item in sub_nodes]))
                return node.score

        return __get_score(self.root_node)


logger.debug("test")
node1 = AHP.Node(score=80)
node2 = AHP.Node(score=86)
node3 = AHP.Node(score=98)
jd_mat = np.array([[1., 3., 5.], [1. / 3., 1., 2.], [1. / 5., 1. / 2., 1.]]).T
node_1 = AHP.Node(jd_mat=jd_mat, sub_nodes=[node1, node2, node3])
node1 = AHP.Node(score=86)
node2 = AHP.Node(score=77)
node3 = AHP.Node(score=90)
node_2 = AHP.Node(jd_mat=jd_mat, sub_nodes=[node1, node2, node3])
node = AHP.Node(jd_mat=[[1., 5.], [1. / 5., 1.]], sub_nodes=[node_1, node_2])
ahp = AHP(node, False)
logger.debug(ahp.evaluate(True))
logger.debug(node.to_string())
