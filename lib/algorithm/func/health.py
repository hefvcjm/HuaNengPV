# coding = utf-8
import numpy as np
from lib.algorithm.func.calculation import fault_score, efficiency_score, temperature_score, group_health
from lib.algorithm.AHP.AHP import AHP

__serial_jd_mat = np.array([[1., 5., 1 / 3.],
                            [1. / 5., 1., 1 / 7.],
                            [3., 7., 1.]]).T

__box_jd_mat = np.array([[1., 5., 1 / 3.],
                         [1. / 5., 1., 1 / 7.],
                         [3., 7., 1.]]).T

__inverter_jd_mat = np.array([[1., 5., 1 / 3.],
                              [1. / 5., 1., 1 / 7.],
                              [3., 7., 1.]]).T

__station_jd_mat = np.array([[1., 5., 1 / 3.],
                             [1. / 5., 1., 1 / 7.],
                             [3., 7., 1.]]).T

__serial_fault_score_params = {"mu": 0.5, "sigma": 0.5, "M": 0.5, "a": 3}
__box_fault_score_params = {"mu": 0.5, "sigma": 0.5, "M": 0.5, "a": 3}
__inverter_fault_score_params = {"mu": 0.5, "sigma": 0.5, "M": 0.5, "a": 3}

__serial_loss_score_params = {"arfa": 0.5, "belta": 0.5, "M": 0.5, "a": 0.5, "b": 0.5}
__box_loss_score_params = {"arfa": 0.5, "belta": 0.5, "M": 0.5, "a": 0.5, "b": 0.5}
__inverter_loss_score_params = {"arfa": 0.5, "belta": 0.5, "M": 0.5, "a": 0.5, "b": 0.5}

__serial_temp_score_params = {"sigma": 0.5, "M": 0.5, "a": 0.5, "b": 0.5, "c": 0.5, "d": 0.5}
__box_temp_score_params = {"sigma": 0.5, "M": 0.5, "a": 0.5, "b": 0.5, "c": 0.5, "d": 0.5}
__inverter_temp_score_params = {"sigma": 0.5, "M": 0.5, "a": 0.5, "b": 0.5, "c": 0.5, "d": 0.5}


def health_evaluate(serials, boxes, inverters):
    """
    健康度评估
    :param serials: 组串数据列表[{id:_id, data:[fault_count, loss, temp]}...]
    :param boxes: 汇流箱数据列表 [{id:_id, data:[fault_count, loss, temp]}...]
    :param inverters: 逆变器数据列表 [{id:_id, data:[fault_count, loss, temp]}...]
    :return:
    """
    serial_scores = []
    for serial in serials:
        data = serial["data"]
        fault_node = AHP.Node(name="fault", score=fault_score(data[0], **__serial_fault_score_params))
        loss_node = AHP.Node(name="loss", score=efficiency_score(data[1], **__serial_loss_score_params))
        temp_node = AHP.Node(name="temp", score=temperature_score(data[2], **__serial_temp_score_params))
        serial_node = AHP.Node(name=serial["id"], jd_mat=__serial_jd_mat, sub_nodes=[fault_node, loss_node, temp_node])
        ahp = AHP(serial_node, False)
        serial_scores.append({"id": serial["id"], "score": ahp.evaluate(True)})

    box_scores = []
    for box in boxes:
        data = box["data"]
        fault_node = AHP.Node(name="fault", score=fault_score(data[0], **__box_fault_score_params))
        loss_node = AHP.Node(name="loss", score=efficiency_score(data[1], **__box_loss_score_params))
        temp_node = AHP.Node(name="temp", score=temperature_score(data[2], **__box_temp_score_params))
        box_node = AHP.Node(name=box["id"], jd_mat=__box_jd_mat, sub_nodes=[fault_node, loss_node, temp_node])
        ahp = AHP(box_node, False)
        box_scores.append({"id": box["id"], "score": ahp.evaluate(True)})

    inverter_scores = []
    for inverter in inverters:
        data = inverter["data"]
        fault_node = AHP.Node(name="fault", score=fault_score(data[0], **__inverter_fault_score_params))
        loss_node = AHP.Node(name="loss", score=efficiency_score(data[1], **__inverter_loss_score_params))
        temp_node = AHP.Node(name="temp", score=temperature_score(data[2], **__inverter_temp_score_params))
        inverter_node = AHP.Node(name=inverter["id"], jd_mat=__inverter_jd_mat,
                                 sub_nodes=[fault_node, loss_node, temp_node])
        ahp = AHP(inverter_node, False)
        inverter_scores.append({"id": inverter["id"], "score": ahp.evaluate(True)})

    group_scores = list()
    group_scores.append({"id": "serials", "score": group_health([item["score"] for item in serial_scores])})
    group_scores.append({"id": "boxes", "score": group_health([item["score"] for item in box_scores])})
    group_scores.append({"id": "inverters", "score": group_health([item["score"] for item in inverter_scores])})

    serials_node = AHP.Node(name="serials", score=group_scores[0]["score"])
    boxes_node = AHP.Node(name="boxes", score=group_scores[0]["score"])
    inverters_node = AHP.Node(name="inverters", score=group_scores[0]["score"])
    station_node = AHP.Node(name="station", jd_mat=__station_jd_mat,
                            sub_nodes=[serials_node, boxes_node, inverters_node])
    ahp = AHP(station_node, False)
    station_score = [{"id": "station", "score": ahp.evaluate(True)}]
    return {"serial": serial_scores, "box": box_scores, "inverter": inverter_scores, "group": group_scores,
            "station": station_score}
