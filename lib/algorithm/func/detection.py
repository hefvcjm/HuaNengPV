# coding = utf-8
import numpy as np
import pandas as pd
import datetime


def serial_zero_current(currents: list or np.array, counts: list or np.array):
    """
    支路电流为零，连续num次电流小于theta认为电流为零。需要记住count，每次调用需要传该参数
    :param currents: 电流 [#X光伏子阵汇流箱X IX1 ,#X光伏子阵汇流箱X IX1, ...]
    :param counts: 累计次数 [上次返回的结果count，每条支路单独一个值]
    :return: 是否发生电流为零故障，count
    -----------------------------------------------------
    参数说明如上所述
    触发条件：实时触发
    """
    theta = 0.01
    num = 5
    currents = np.array(currents)
    counts = np.array(counts)
    counts[currents < theta] += 1
    counts[currents >= theta] = 0
    result = dict()
    result["result"] = (counts >= num).tolist()
    counts[counts >= num] = num - 1
    result["count"] = counts.tolist()
    return result


def serial_current_low(currents, start_times, now=None) -> dict:
    """
    支路电流偏低
    :param currents: 同一个汇流箱下的支路电流 [#X光伏子阵汇流箱X I1,#X光伏子阵汇流箱X I2, #X光伏子阵汇流箱X I3 ...]
    :param start_times: 支路电流偏低开始时间，由返回的中间结果得到 [上次返回的结果start_times，每条支路单独一个值]
    :param now: 当前时刻
    :return: 结果信息pd.DataFrame,包含字段results：此次诊断结果；start_times：更新后得开始时间；delta_times：连续偏低时间；diagnosis_results：最终结果，delta_times > 10,为1，否则为0
    -----------------------------------------------------
    参数说明如上所述
    触发条件：实时触发
    """
    if now is None:
        now = datetime.datetime.time()
    threshold = 10
    I = np.array(currents)
    mu = np.mean(I)
    sigma = np.std(I)
    results = (I - mu > 3 * sigma) & (sigma > 0.3)
    delta_times = (np.datetime64(now, "s") - np.array([np.datetime64(i, "s") for i in start_times])).astype(int) / 3600
    df = pd.DataFrame(np.array([results, [np.datetime64(i, "s") for i in start_times], delta_times]).T,
                      columns=["results", "start_times", "delta_times"])
    df.loc[df["results"] == False, "start_times"] = now
    df.loc[df["results"] == False, "delta_times"] = 0
    df["diagnosis_results"] = False
    df.loc[df["delta_times"] > threshold, "diagnosis_results"] = True
    temp = df.to_dict(orient="split")
    return dict(zip(temp["columns"], np.array(temp["data"]).T.tolist()))
