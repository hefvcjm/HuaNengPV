# coding = utf-8
# 模拟计算光伏理论输出
# todo: 是否有解判断，错误提示，参数校验
import math
import numpy as np


def get_i_by_u(Iph, Io, n, Rsh, Rs, T, U, Uoc=None, Isc=None):
    if Uoc is None or Isc is None:
        Uoc, Isc = get_voc_isc(Iph, Io, n, Rsh, Rs, T)
    q = 1.6 * (10 ** -19)
    k = 1.38 * (10 ** -23)
    e = 0.01
    Ib = 0
    Iu = Isc
    err_last = None
    step = 5
    I = step
    err = I - Iph + Io * (math.exp(q * (U + Rs * I) / (n * k * T * 60)) - 1) + (U + I * Rs) / Rsh
    while abs(err) > e:
        if err_last is not None:
            if err_last * err < 0:
                Ib = I - step
                Iu = I
                break
        err_last = err
        I = I + step
        err = I - Iph + Io * (math.exp(q * (U + Rs * I) / (n * k * T * 60)) - 1) + (U + I * Rs) / Rsh
    I = (Iu + Ib) / 2
    err = I - Iph + Io * (math.exp(q * (U + Rs * I) / (n * k * T * 60)) - 1) + (U + I * Rs) / Rsh
    while abs(err) > e:
        if err > 0:
            Iu = I
        else:
            Ib = I
        I = (Iu + Ib) / 2
        err = I - Iph + Io * (math.exp(q * (U + Rs * I) / (n * k * T * 60)) - 1) + (U + I * Rs) / Rsh
    return I


def get_voc_isc(Iph, Io, n, Rsh, Rs, T):
    q = 1.6 * (10 ** -19)
    k = 1.38 * (10 ** -23)
    e = 0.01
    step = 5
    Ib = 0
    Iu = step
    err_last = None
    step = 5
    I = 0
    err = I - Iph + Io * (math.exp(q * (Rs * I) / (n * k * T * 60)) - 1) + (I * Rs) / Rsh
    while abs(err) > e:
        if err_last is not None:
            if err_last * err < 0:
                Ib = I - step
                Iu = I
                break
        err_last = err
        I = I + step
        err = I - Iph + Io * (math.exp(q * (Rs * I) / (n * k * T * 60)) - 1) + (I * Rs) / Rsh
    I = (Iu + Ib) / 2
    err = I - Iph + Io * (math.exp(q * (Rs * I) / (n * k * T * 60)) - 1) + (I * Rs) / Rsh
    while abs(err) > e:
        # print(err)
        if err > 0:
            Iu = I
        else:
            Ib = I
        I = (Iu + Ib) / 2
        err = I - Iph + Io * (math.exp(q * (Rs * I) / (n * k * T * 60)) - 1) + (I * Rs) / Rsh
    Isc = I
    U = 0
    err = - Iph + Io * (math.exp(q * U / (n * k * T * 60)) - 1) + U / Rsh
    while abs(err) > e:
        if err_last is not None:
            if err_last * err < 0:
                Ib = U - step
                Iu = U
                break
        err_last = err
        U = U + step
        err = - Iph + Io * (math.exp(q * U / (n * k * T * 60)) - 1) + U / Rsh
    U = (Iu + Ib) / 2
    err = - Iph + Io * (math.exp(q * U / (n * k * T * 60)) - 1) + U / Rsh
    while abs(err) > e:
        # print(err)
        if err > 0:
            Iu = U
        else:
            Ib = U
        U = (Iu + Ib) / 2
        err = - Iph + Io * (math.exp(q * U / (n * k * T * 60)) - 1) + U / Rsh
    Uoc = U
    return Uoc, Isc


def get_max_power_point(Iph, Io, n, Rsh, Rs, T):
    Uoc, Isc = get_voc_isc(Iph, Io, n, Rsh, Rs, T)
    Us = np.linspace(0, Uoc * 0.9, 1000)
    Is = [get_i_by_u(Iph, Io, n, Rsh, Rs, T, u, Uoc, Isc) for u in Us]
    Is = np.array(Is)
    Ps = Us * Is
    max_p = max(Ps)
    index = np.where(Ps == max_p)[0][0]
    # print(index)
    return max_p, Us[index], Is[index]


def get_iph(Isc, alpha, Tref, Sref, T, S):
    return (Isc + alpha * (T - Tref)) * S / Sref


def get_isc(Isc_ref, Rsh, Rs):
    return Isc_ref * (Rsh + Rs) / Rsh


def get_io(Isc_ref, Uoc_ref, alpha, beta, Tref, n, T):
    q = 1.6 * (10 ** -19)
    k = 1.38 * (10 ** -23)
    return (Isc_ref + alpha * (T - Tref)) / (math.exp(q * (Uoc_ref + beta * (T - Tref)) / (n * k * T * 60)) - 1)


def get_rsh(Rsh_ref, Sref, S):
    return Rsh_ref * Sref / S
