#!/usr/bin/env python3

import csv
import re

with open('ori_data', mode='r', encoding='utf-8', newline='') as csv_in_file:
    with open('dea_data_output', mode='w', newline='') as out_file:
        filereader = csv.reader(csv_in_file)
        for row_list in filereader:
            # 创建要写入输出文件的输出字符串
            out_str = ''

            # 删去共有的无用信息
            row_list.pop()
            row_list.pop(2)
            row_list.pop(3)

            # 修改前三列的数据
            row_list[0] = re.search(r'Tue Mar 19', row_list[0]).group()
            row_list[1] = ''.join(row_list[1].split())
            row_list[1] = ''.join(row_list[1].replace('>', '').replace('租房', '  ').replace('网', '').rstrip())
            row_list[2] = re.search(r'(\d*)元/月', row_list[2]).group()

            # 根据列表长度删去各自的无用信息
            if len(row_list) == 9:
                row_list.pop()
                row_list.pop()
                row_list.pop()
                row_list.pop()
                row_list.pop()
            elif len(row_list) == 8:
                row_list.pop()
                row_list.pop()
                row_list.pop()
                row_list.pop()
            elif len(row_list) == 7:
                row_list.pop()
                row_list.pop()
                row_list.pop()
            elif len(row_list) == 6:
                row_list.pop()
                row_list.pop()

            # 修改最后一列的信息
            if row_list[-1].strip() == 'None':
                row_list[-1] = 'NULL NULL NULL NULL NULL NULL NULL NULL NULL NULL NULL NULL NULL NULL'
            else:
                s = ''
                # 房屋面积
                s += re.search(r'(\d*㎡)', row_list[-1]).group()
                s += ' '
                # 室、卫、厅
                s += re.search(r'(\d*室)', row_list[-1]).group()
                s += ' '
                s += re.search(r'(\d*卫)', row_list[-1]).group()
                s += ' '
                s += re.search(r'(\d*厅)', row_list[-1]).group()
                s += ' '
                # 房屋朝向
                s += re.search(r'朝\w', row_list[-1]).group()
                s += ' '
                # 所在楼层
                if re.search(r'(\d*/\d*层)', row_list[-1]) is None:
                    s += 'NULL'
                else:
                    if re.search(r'(\d*/\d*层)', row_list[-1]).group()[0] == '/':
                        s += 'NULL'
                    else:
                        s += re.search(r'(\d*/\d*层)', row_list[-1]).group()
                s += ' '
                # 租期
                if re.search(r'(\d*~\d*年)', row_list[-1]) is None:
                    s += 'NULL'
                else:
                    s += re.search(r'(\d*~\d*年)', row_list[-1]).group()
                s += ' '
                # 入住
                if re.search(r'随时入住', row_list[-1]) is None:
                    s += 'NULL'
                else:
                    s += re.search(r'随时入住', row_list[-1]).group()
                s += ' '
                # 电梯
                if re.search(r'电梯：有', row_list[-1]):
                    s += '有 '
                elif re.search(r'电梯：无', row_list[-1]):
                    s += '无 '
                elif re.search(r'电梯：暂无数据', row_list[-1]):
                    s += '暂无 '
                # 车位
                if re.search(r'车位：免费', row_list[-1]):
                    s += '免费 '
                elif re.search(r'车位：租用', row_list[-1]):
                    s += '租用 '
                elif re.search(r'车位：暂无数据', row_list[-1]):
                    s += '暂无 '
                # 用水
                if re.search(r'用水：民水', row_list[-1]):
                    s += '民水 '
                elif re.search(r'用水：商水', row_list[-1]):
                    s += '商水 '
                elif re.search(r'用水：暂无数据', row_list[-1]):
                    s += '暂无 '
                # 用电
                if re.search(r'用电：民电', row_list[-1]):
                    s += '民电 '
                elif re.search(r'用电：商电', row_list[-1]):
                    s += '商电 '
                elif re.search(r'用电：暂无数据', row_list[-1]):
                    s += '暂无 '
                # 燃气
                if re.search(r'燃气：有', row_list[-1]):
                    s += '有 '
                elif re.search(r'燃气：无', row_list[-1]):
                    s += '无 '
                elif re.search(r'燃气：暂无数据', row_list[-1]):
                    s += '暂无 '
                # 采暖
                if re.search(r'采暖：自采暖', row_list[-1]):
                    s += '自采暖'
                elif re.search(r'采暖：集中供暖', row_list[-1]):
                    s += '集中'
                elif re.search(r'采暖：暂无数据', row_list[-1]):
                    s += '暂无'
                row_list[-1] = s

            # 向输出字符串内添加信息
            out_str += row_list[0] + ' ' + row_list[1] + ' ' + row_list[2] + ' ' + row_list[3] + '\n'

            # 写入文件
            out_file.write(out_str)
