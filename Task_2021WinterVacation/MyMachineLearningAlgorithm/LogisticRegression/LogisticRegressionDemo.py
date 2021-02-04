import MyLogisticRegression as MyLR


data = []
labels = []
with open('./testSet.txt', 'r') as fr:
    for line in fr.readlines():
        line_arr = line.strip().split()
        data.append([1.0, float(line_arr[0]), float(line_arr[1])])
        labels.append(int(line_arr[2]))

weights = MyLR.gradAscent(data, labels)
MyLR.plotBestFit(weights, data, labels)
