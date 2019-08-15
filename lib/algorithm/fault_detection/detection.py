# coding = utf-8
import numpy as np
import pandas as pd
import datetime


def serial_zero_current(current, count):
    """
    支路电流为零，连续num次电流小于theta认为电流为零。需要记住count，每次调用需要传该参数
    :param current: 电流
    :param count: 累计次数
    :return: 是否发生电流为零故障，count
    """
    theta = 0.01
    num = 2
    if current < theta:
        count += 1
    else:
        count = 0
        return False, count
    if count < num:
        return False, count
    else:
        count = 1
        return True, count


def serial_current_low(currents, start_times, now=datetime.datetime.time()) -> pd.DataFrame:
    """
    支路电流偏低
    :param currents: 同一个汇流箱下的支路电流
    :param start_times: 支路电流偏低开始时间，由返回的中间结果得到
    :param now: 当前时刻
    :return: 结果信息pd.DataFrame,包含字段results：此次诊断结果；start_times：更新后得开始时间；delta_times：连续偏低时间；diagnosis_results：最终结果，delta_times > 10,为1，否则为0
    """
    threshold = 10
    I = np.array(currents)
    mu = np.mean(I)
    sigma = np.std(I)
    results = (I - mu > 3 * sigma) & (sigma > 0.3)
    delta_times = np.datetime64(now, "s") - np.array(start_times, "s") / 3600
    df = pd.DataFrame(np.array([results, np.array(start_times, "s"), delta_times]).T,
                      columns=["results", "start_times", "delta_times"])
    df.loc[df["results"] == False, "start_times"] = now
    df["diagnosis_results"] = 0
    df.loc[df["results"] == False, "delta_times"] = 0
    df.loc[df["delta_times"] > threshold, "diagnosis_results"] = 1
    return df
