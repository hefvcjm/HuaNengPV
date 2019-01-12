# 故障诊断配置信息

# 某一支路电流为零配置
config_serial_current_zero = {
    "zero_bias": 0.3,  # 为零误差偏置
    "zero_rate": 0.8,  # 横向比较结果阈值
    "counter": 5,  # 累计次数
}

# 支路电流偏低
config_serial_current_low = {
    "counter": 5,  # 累计次数
}

# 所有支路电流为零
config_serial_current_all_zero = {
    "box_bias": 0.4,  # 汇流箱输出电流为零误差偏置
    "serial_bias": 0.3,  # 支路电流为零误差偏置
    "box_counter": 5,  # 汇流箱累计次数
    "serial_rate": 0.6,  # 支路电流小于阈值比例
}

# 汇流箱母线电压偏低
config_combiner_box_voltage_low = {
    "counter": 5,  # 累计次数
}

# 逆变器过温
config_converter_over_temp = {
    "high_bias": 100,  # 死区上限
    "low_bias": 90,  # 死区下限
}

# 逆变器交流频率故障
config_converter_freq_fault = {
    "high_bias": 50.3,  # 频率上限
    "low_bias": 49.7,  # 频率下限
}

# 逆变器交流过压或欠压
config_converter_voltage_fault = {
    "high_bias": 500,  # 上限
    "low_bias": 450,  # 下限
}

# 逆变器输出功率偏低
config_converter_power_low = {
    "rate": 0.8,  # 比例系数
}

# 逆变器输出效率偏低
config_converter_efficiency_low = {
    "efficiency": 0.98,  # 逆变器效率
}
