#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv


with open('TianjinRentHouseInfo.csv', 'r', newline='') as csv_in_file:
    with open('ProcessedTianjinRentHouseInfo.csv', 'w', newline='') as csv_out_file:
        filereader = csv.reader(csv_in_file)
        filewriter = csv.writer(csv_out_file)
        header = next(filereader)
        new_header = ['所在城市', '所在区县', '所在街道或地区', '小区名称', '面积', '租赁方式', '朝向', '月租', '计费方式', '室',
                      '厅', '卫', '入住', '租期', '看房', '所在楼层', '总楼层', '电梯', '车位', '用水', '用电', '燃气', '采暖']
        filewriter.writerow(new_header)
        for row_list in filereader:
            if '新区' in row_list[2]:    # 统一所在区县格式
                row_list[2] = row_list[2].replace('新区', '')
            elif '区' in row_list[2]:
                row_list[2] = row_list[2].replace('区', '')
            row_list[5] = row_list[5][:-1]    # 去除面积的单位
            row_list[7] = row_list[7][0]    # 只保留朝向的第一个方位
            row_list[8] = row_list[8].replace('元/月', '')    # 去除月租的单位
            row_list[10] = row_list[10].replace('室', '')    # 去除室的单位
            row_list[11] = row_list[11].replace('厅', '')    # 去除厅的单位
            row_list[12] = row_list[12].replace('卫', '')    # 去除卫的单位
            if row_list[13] != '随时入住':    # 如果入住有具体时间，将其统一为yyyymmdd格式
                check_in_list = row_list[13].split('-')
                row_list[13] = ''.join(check_in_list)
            row_list[17] = row_list[17].replace('层', '')    # 去除总楼层的单位
            if row_list[16] != '高楼层' and row_list[16] != '中楼层' and row_list[16] != '低楼层':    # 统一所在楼层格式
                if int(row_list[16]) <= int(row_list[17]) / 3:
                    row_list[16] = '低楼层'
                elif int(row_list[17]) / 3 < int(row_list[16]) < int(row_list[17]) / 3 * 2:
                    row_list[16] = '中楼层'
                else:
                    row_list[16] = '高楼层'
            row_list.pop(0)    # 不保留房源编号
            filewriter.writerow(row_list)
    print('写入成功')
