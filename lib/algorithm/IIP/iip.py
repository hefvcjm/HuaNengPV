# coding = utf-8

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

_row = 28

_num_name = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-"]
_num_template = []
for name in _num_name:
    t = cv2.imread("template/%s.jpg" % name, cv2.IMREAD_GRAYSCALE)
    ret, t = cv2.threshold(t, 50, 255, cv2.THRESH_BINARY)
    t[t == 255] = 1
    _num_template.append(t)
_min_col = min([item.shape[1] for item in _num_template])


class iip:
    """
    红外图像最高温度提取并计算平均温度
    """

    def __init__(self, image_path: str, up_temp_area: tuple = ((36, 375), (64, 480)),
                 down_temp_area: tuple = ((526, 375), (554, 480)),
                 color_strip_area: tuple = ((464, 74), (474, 518))):
        """
        构造函数，其中(lt_x,lt_y)为左上角坐标，(rb_x,rb_y)右下角坐标
        :param image_path:红外图像路径
        :param up_temp_area:上温度数字矩形区域，((lt_x,lt_y),(rb_x,rb_y))
        :param down_temp_area:下温度数字矩形区域，((lt_x,lt_y),(rb_x,rb_y))
        :param color_strip_area:比色条矩形区域，((lt_x,lt_y),(rb_x,rb_y))
        """
        self.up_temp_area = up_temp_area
        self.down_temp_area = down_temp_area
        self.color_strip_area = color_strip_area
        self.image = cv2.imread(image_path)
        # print(self.image.shape)
        # cv2.imshow("color", self.image)
        # cv2.waitKey(0)
        self.up_temp, self.down_temp = self.__get_up_down_temp()
        print(self.up_temp, self.down_temp)

    def __get_temp_range(self) -> tuple:
        """
        根据图像温度上下限获取获取红外图像中温度范围
        :return:红外图像上下限(up_temp,down_temp)
        """
        self.up_temp = 21.2
        self.down_temp = -9.2

    def __get_map_param(self) -> tuple:
        """
        获取像素RGB到温度映射的参数，假设为线性关系
        :return: R、G、B通道映射的参数(p_r,p_g,p_b)
        """
        ((lt_x, lt_y), (rb_x, rb_y)) = self.color_strip_area
        color_strip = self.image[lt_y:rb_y, lt_x:rb_x, :]
        b, g, r = cv2.split(color_strip)
        df_r = pd.DataFrame(r)
        df_g = pd.DataFrame(g)
        df_b = pd.DataFrame(b)
        df_rgb = pd.DataFrame(
            {"r": df_r.mean(axis=1), "g": df_g.mean(axis=1), "b": df_b.mean(axis=1),
             "sum": df_r.mean(axis=1) + df_g.mean(axis=1) + df_b.mean(axis=1)})
        df_rgb_diff = df_rgb.diff()
        temp_flag = (df_rgb_diff < 20) & (df_rgb_diff > -20)
        temp_flag_ = temp_flag["r"]
        for col in temp_flag.iteritems():
            temp_flag_ = temp_flag_ & col[1]
        index = temp_flag_[temp_flag_ == False].index.to_series()
        print(index.tolist())
        sep = 40
        left = index.tolist()[0]
        right = left + sep
        max_count = 0
        for i in index.tolist()[1:-1]:
            size_ = index[index > left][index < right].size
            # print(index[index > left][index < right])
            if size_ > max_count:
                max_count = size_
                left = i
                right = min(left + sep, index.tolist()[-1])
        left = index[index > left][index < right].tolist()[0]
        right = index[index > left][index < right].tolist()[-1]
        df_rgb[left - 3:right + 3, :] = np.nan

        return (1, 2, 3)

    def get_map_param(self):
        """
        获取像素RGB到温度映射的参数，假设为线性关系
        :return: R、G、B通道映射的参数(p_r,p_g,p_b)
        """
        ((lt_x, lt_y), (rb_x, rb_y)) = self.color_strip_area
        color_strip = self.image[lt_y:rb_y, lt_x:rb_x, :]
        # color_strip = cv2.cvtColor(color_strip, cv2.COLOR_BGR2HSV)
        b, g, r = cv2.split(color_strip)
        df_rgb = pd.DataFrame({"r": r.mean(axis=1), "g": g.mean(axis=1), "b": b.mean(axis=1)})
        df_rgb_diff = df_rgb.diff()
        df_rgb_diff.plot()
        plt.show()
        bool_flag = (df_rgb_diff > 20) | (df_rgb_diff < -20)
        flag = bool_flag["r"] | bool_flag["g"] | bool_flag["b"]
        flag_temp = flag[flag]
        index = flag_temp.index.to_series()
        sep = 40
        left = index.tolist()[0]
        right = left + sep
        max_count = index[index > left][index < right].size
        print(index.tolist())
        for i in index.tolist()[1:-1]:
            size_ = index[index > left][index < right].size
            if max_count < size_:
                max_count = size_
                left = i
                right = left + sep
        left = index[index > left][index < right].tolist()[0]
        right = index[index > left][index < right].tolist()[-1]
        df_rgb.loc[left - 5:right + 5, :] = np.nan
        df_rgb = df_rgb.interpolate("linear")
        df_rgb = df_rgb - self.image[300, 300, :][::-1]
        print(min((df_rgb["r"] ** 2 + df_rgb["g"] ** 2 + df_rgb["b"] ** 2) ** 0.5))
        plt.plot((df_rgb["r"] ** 2 + df_rgb["g"] ** 2 + df_rgb["b"] ** 2) ** 0.5)
        df_rgb.plot()
        plt.show()

    def __ocr_number(self, num_area: np.array) -> float:
        col = num_area.shape[1]
        conv_result = np.zeros((len(_num_template), num_area.shape[1]))
        result = []
        i = 0
        j = 0
        while j < col:
            i = 0
            for template in _num_template:
                _col = template.shape[1]
                _num = num_area[:, j:j + _col]
                if _num.shape[1] < _col:
                    continue
                mol = np.sum((_num - np.mean(_num)) * (template - np.mean(template)))
                den = (np.sum((_num - np.mean(_num)) ** 2) * (np.sum((template - np.mean(template)) ** 2))) ** 0.5
                conv_result[i, j] = mol / den
                if conv_result[i, j] > 0.95:
                    result.append(_num_name[i])
                    j += _min_col - 1
                    break
                i += 1
            j += 1
        conv_result[np.isnan(conv_result)] = 0
        # max_col = conv_result.max(axis=0)
        # print(max_col)
        # print(result)
        # plt.plot(max_col)
        # plt.show()
        return float(''.join(result[:-1]) + "." + result[-1])

    def __get_up_down_temp(self) -> tuple:
        ((lt_x, lt_y), (rb_x, rb_y)) = self.up_temp_area
        _area = cv2.cvtColor(self.image[lt_x:rb_x, lt_y:rb_y, :], cv2.COLOR_BGR2GRAY)
        ret, _area = cv2.threshold(_area, 50, 255, cv2.THRESH_BINARY)
        up_temp = self.__ocr_number(_area)
        ((lt_x, lt_y), (rb_x, rb_y)) = self.down_temp_area
        _area = cv2.cvtColor(self.image[lt_x:rb_x, lt_y:rb_y, :], cv2.COLOR_BGR2GRAY)
        ret, _area = cv2.threshold(_area, 50, 255, cv2.THRESH_BINARY)
        down_temp = self.__ocr_number(_area)
        return up_temp, down_temp


iip(r"E:\project\HuaNengPV\infrared_images\41-1-4-12-serial\IR000186.JPG").get_map_param()

# def ocr_number(num_area: np.array) -> float:
#     col = num_area.shape[1]
#     conv_result = np.zeros((len(_num_template), num_area.shape[1]))
#     result = []
#     i = 0
#     j = 0
#     while j < col:
#         i = 0
#         for template in _num_template:
#             _col = template.shape[1]
#             _num = num_area[:, j:j + _col]
#             if _num.shape[1] < _col:
#                 continue
#             mol = np.sum((_num - np.mean(_num)) * (template - np.mean(template)))
#             den = (np.sum((_num - np.mean(_num)) ** 2) * (np.sum((template - np.mean(template)) ** 2))) ** 0.5
#             conv_result[i, j] = mol / den
#             if conv_result[i, j] > 0.95:
#                 result.append(_num_name[i])
#                 j += _min_col - 1
#                 break
#             i += 1
#         j += 1
#     conv_result[np.isnan(conv_result)] = 0
#     # max_col = conv_result.max(axis=0)
#     # print(max_col)
#     # print(result)
#     # plt.plot(max_col)
#     # plt.show()
#     return float(''.join(result[:-1]) + "." + result[-1])
#
#
# image = cv2.imread(r"E:\project\HuaNengPV\infrared_images\41-1-4-12-serial\IR000190.JPG")
# # # 36:64, 400:422, :
# # 36:64, 375:480, :   上温度区域
# #
# num = image[526:554, 375:480, :]
# gray_num = cv2.cvtColor(num, cv2.COLOR_BGR2GRAY)
# ret, thr = cv2.threshold(gray_num, 50, 255, cv2.THRESH_BINARY)
# print(ocr_number(thr))
# cv2.imshow("image", thr)
# cv2.waitKey(0)
