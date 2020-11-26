#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv


high_temp_list = []
high_temp_list1 = []
high_temp_list2 = []
high_temp_dict = {}
with open('./WeatherData.csv', 'r', encoding='gbk', newline='') as ori_data:
    filereader = csv.reader(ori_data)
    header = next(filereader)
    for row_list in filereader:
        high_temp_list.append(int(row_list[2].replace('℃', '')))
        if row_list[0][5:] not in high_temp_dict:
            high_temp_dict[row_list[0][5:]] = [int(row_list[2].replace('℃', '')), 1]
        else:
            high_temp_dict[row_list[0][5:]][0] += int(row_list[2].replace('℃', ''))
            high_temp_dict[row_list[0][5:]][1] += 1
    high_temp_list1 = high_temp_list.copy()
    high_temp_list1.insert(0, '-')
    high_temp_list1.pop()
    high_temp_list2 = high_temp_list1.copy()
    high_temp_list2.insert(0, '-')
    high_temp_list2.pop()

high_temp_average_dict = {}
for key in high_temp_dict:
    high_temp_average_dict[key] = '%.1f' % (high_temp_dict[key][0] / high_temp_dict[key][1])

with open('./WeatherData.csv', 'r', encoding='gbk', newline='') as ori_data:
    with open('./WeatherData_Processed.csv', 'w', newline='') as dea_data:
        filereader = csv.reader(ori_data)
        filewriter = csv.writer(dea_data)
        header = next(filereader)
        filewriter.writerow(['year', 'month', 'day', 'week', 'high_temp_2', 'high_temp_1', 'average', 'actual'])
        cnt = 0
        for row_list in filereader:
            new_info_list = []
            new_info_list.extend(row_list[0].split('-'))
            week_dict = {
                '星期一': 'Mon',
                '星期二': 'Tue',
                '星期三': 'Wed',
                '星期四': 'Thu',
                '星期五': 'Fri',
                '星期六': 'Sat',
                '星期日': 'Sun'
            }
            new_info_list.append(week_dict[row_list[1]])
            new_info_list.extend([high_temp_list2[cnt], high_temp_list1[cnt], high_temp_average_dict[row_list[0][5:]],
                                  high_temp_list[cnt]])
            cnt += 1
            if cnt == 1 or cnt == 2:
                continue
            filewriter.writerow(new_info_list)
