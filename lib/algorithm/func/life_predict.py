# coding = utf-8
from lib.algorithm.GM.gm import gm

__max_life = 100  # 最大年限


def life_predict(aging_rates: list):
    """
    设备寿命预测(年)
    :param aging_rates: 历史年老化率列表
    :return:
    """
    if len(aging_rates) < 3:
        return None
    model = gm(aging_rates)
    return model.predict_all(__max_life)
