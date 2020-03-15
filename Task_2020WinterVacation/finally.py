#!/usr/bin/env python3

import csv
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, 'r', newline='') as csv_in_file:
    with open(output_file, 'w', newline='') as csv_out_file:
        filereader = csv.reader(csv_in_file)
        filewriter = csv.writer(csv_out_file)
        total = []
        for row_list in filereader:
            total.append(row_list[0])
        outputList = []
        a_list = []
        a = 0
        for data in total:
            if a < 19:
                a += 1
                a_list.append(data)
            else:
                a_list.append(data)
                outputList.append(a_list)
                a = 0
                a_list = []
        for output_line in outputList:
            filewriter.writerow(output_line)
