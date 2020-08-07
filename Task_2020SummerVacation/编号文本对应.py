#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
import re


def LabelData(elem, labeled_col_list, labeled_dic, label):
    """
    对大量数据自动编号
    :return: 元组，其中的元素为最终编号和下一待编号
    """
    if elem not in labeled_col_list:
        labeled_col_list.append(elem)
        ret = label
        labeled_dic[elem] = ret
        label += 1
    else:
        ret = labeled_col_list.index(elem) + 1
    return ret, label


# 对所在区县、所在街道或地区、小区名称编号使用的变量
labeled_col_1, labeled_col_2, labeled_col_3 = [], [], []
labeled_dic_1, labeled_dic_2, labeled_dic_3 = {}, {}, {}
label1, label2, label3 = 1, 1, 1
# 计算租期的均值所用的求和变量
total_term = 0
# 存储各行信息列表的列表
rows = []

with open('ProcessedTianjinRentHouseInfo.csv', 'r', newline='') as csv_in_file:
    filereader = csv.reader(csv_in_file)

    # 读取标题行
    head = next(filereader)

    for row_list in filereader:
        # 所在城市
        row_list[0] = 1
        # 所在区县
        row_1_data = LabelData(row_list[1], labeled_col_1, labeled_dic_1, label1)
        row_list[1] = row_1_data[0]
        label1 = row_1_data[1]
        # 所在街道或地区
        row_2_data = LabelData(row_list[2], labeled_col_2, labeled_dic_2, label2)
        row_list[2] = row_2_data[0]
        label2 = row_2_data[1]
        # 小区名称
        row_3_data = LabelData(row_list[3], labeled_col_3, labeled_dic_3, label3)
        row_list[3] = row_3_data[0]
        label3 = row_3_data[1]

print(labeled_dic_1)
print(labeled_dic_2)
print(labeled_dic_3)
