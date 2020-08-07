#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
import re


def LabelData(elem, labeled_col_list, label):
    """
    对大量数据自动编号
    :return: 元组，其中的元素为最终编号和下一待编号
    """
    if elem not in labeled_col_list:
        labeled_col_list.append(elem)
        ret = label
        label += 1
    else:
        ret = labeled_col_list.index(elem) + 1
    return ret, label


# 对所在区县、所在街道或地区、小区名称编号使用的变量
labeled_col_1, labeled_col_2, labeled_col_3 = [], [], []
label1, label2, label3 = 1, 1, 1
# 计算租期的均值所用的求和变量
total_term = 0
# 存储各行信息列表的列表
rows = []

with open('ProcessedTianjinRentHouseInfo.csv', 'r', newline='') as csv_in_file:
    with open('LabeledTianjinRentHouseInfo.csv', 'w', newline='') as csv_out_file:
        filereader = csv.reader(csv_in_file)
        filewriter = csv.writer(csv_out_file)

        # 读写标题行
        head = next(filereader)
        filewriter.writerow(head)

        # 第一次处理数据
        for row_list in filereader:
            # 所在城市
            row_list[0] = 1
            # 所在区县
            row_1_data = LabelData(row_list[1], labeled_col_1, label1)
            row_list[1] = row_1_data[0]
            label1 = row_1_data[1]
            # 所在街道或地区
            row_2_data = LabelData(row_list[2], labeled_col_2, label2)
            row_list[2] = row_2_data[0]
            label2 = row_2_data[1]
            # 小区名称
            row_3_data = LabelData(row_list[3], labeled_col_3, label3)
            row_list[3] = row_3_data[0]
            label3 = row_3_data[1]
            # 租赁方式
            if row_list[5] == '整租':
                row_list[5] = 1
            elif row_list[5] == '合租':
                row_list[5] = 2
            # 朝向
            aspect_dic = {
                '东': 1,
                '南': 2,
                '西': 3,
                '北': 4,
                '东南': 5,
                '东北': 6,
                '西南': 7,
                '西北': 8
            }
            row_list[6] = aspect_dic[row_list[6]]
            # 计费方式
            charge_mode_dic = {
                '月付价': 1,
                '季付价': 2,
                '半年付价': 3,
                '年付价': 4,
                'None': 5
            }
            row_list[8] = charge_mode_dic[row_list[8]]
            # 入住
            if row_list[12] == '随时入住':
                row_list[12] = 1
            # 租期
            if row_list[13] != '暂无数据':
                if re.search(r'年', row_list[13]):
                    term = int(re.sub(r'(\D)', ' ', row_list[13]).split()[0]) * 12
                elif re.search(r'月', row_list[13]):
                    term = int(re.sub(r'(\D)', ' ', row_list[13]).split()[0])
                row_list[13] = term
                total_term += term
            # 看房
            see_house_dic = {
                '随时可看': 1,
                '需提前预约': 2,
                '一般下班后可看': 3
            }
            row_list[14] = see_house_dic[row_list[14]]
            # 所在楼层
            floor_dic = {
                '低楼层': 1,
                '中楼层': 2,
                '高楼层': 3
            }
            row_list[15] = floor_dic[row_list[15]]
            # 电梯
            lift_dic = {
                '有': 1,
                '无': 2,
                '暂无数据': 3
            }
            row_list[17] = lift_dic[row_list[17]]
            # 车位
            stall_dic = {
                '暂无数据': 1,
                '免费使用': 2,
                '租用车位': 3
            }
            row_list[18] = stall_dic[row_list[18]]
            # 用水
            water_dic = {
                '民水': 1,
                '商水': 2,
                '暂无数据': 3
            }
            row_list[19] = water_dic[row_list[19]]
            # 用电
            elec_dic = {
                '民电': 1,
                '商电': 2,
                '暂无数据': 3
            }
            row_list[20] = elec_dic[row_list[20]]
            # 燃气
            gas_dic = {
                '有': 1,
                '无': 2,
                '暂无数据': 3
            }
            row_list[21] = gas_dic[row_list[21]]
            # 采暖
            heating_dic = {
                '集中供暖': 1,
                '自采暖': 2,
                '暂无数据': 3
            }
            row_list[22] = heating_dic[row_list[22]]
            # 将第一次处理后的数据保存在rows列表中
            rows.append(row_list)

        # 第二次处理数据
        for row_list in rows:
            # 再次处理暂无数据的租期，将其更改为均值
            if row_list[13] == '暂无数据':
                row_list[13] = total_term // 1503
            # 将处理后的数据写入文件
            filewriter.writerow(row_list)
        print('写入成功')
