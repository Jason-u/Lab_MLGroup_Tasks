#!/usr/bin/env python3

import csv
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

movementsDict = {}
inputData = []
with open(input_file, 'r', newline='') as csv_in_file:
    filereader = csv.reader(csv_in_file)
    movementsList = []
    for row_list in filereader:
        movementsList.append(row_list[1])
    for movement in movementsList:
        if movement not in movementsDict:
            movementsDict[movement] = 1
        else:
            movementsDict[movement] += 1
    for movement, movementsDict[movement] in movementsDict.items():
        print('Movement: %-15s' % movement, end='')
        print('Amount: ' + str(movementsDict[movement]))
        movementsDict[movement] = movementsDict[movement] // 100 * 100
        inputData.append(movementsDict[movement])
    csv_in_file.seek(0, 0)
    with open(output_file, 'w', newline='') as csv_out_file:
        filewriter = csv.writer(csv_out_file)
        countWalking = 0
        countJogging = 0
        countUpstairs = 0
        countDownstairs = 0
        countStanding = 0
        countSitting = 0
        for row_list in filereader:
            if row_list[1] == 'Walking':
                if countWalking < inputData[0]:
                    filewriter.writerow(row_list)
                    countWalking += 1
            elif row_list[1] == 'Jogging':
                if countJogging < inputData[1]:
                    filewriter.writerow(row_list)
                    countJogging += 1
            elif row_list[1] == 'Upstairs':
                if countUpstairs < inputData[2]:
                    filewriter.writerow(row_list)
                    countUpstairs += 1
            elif row_list[1] == 'Downstairs':
                if countDownstairs < inputData[3]:
                    filewriter.writerow(row_list)
                    countDownstairs += 1
            elif row_list[1] == 'Standing':
                if countStanding < inputData[4]:
                    filewriter.writerow(row_list)
                    countStanding += 1
            else:
                if countSitting < inputData[5]:
                    filewriter.writerow(row_list)
                    countSitting += 1
