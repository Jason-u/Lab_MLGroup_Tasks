"""
MyLogisticRegression.py - 基于NumPy和Matplotlib实现逻辑斯谛回归（对数几率回归）
Author: Chen Chunhan
Date  : 2021-2-4
"""
import numpy as np
import matplotlib.pyplot as plt


def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))


def gradAscent(data, labels):
    data_matrix = np.mat(data)
    label_matrix = np.mat(labels).transpose()
    m, n = np.shape(data_matrix)
    alpha = 0.001
    max_cycles = 500
    weights = np.ones((n, 1))
    for i in range(max_cycles):
        h = sigmoid(data_matrix * weights)
        error = label_matrix - h
        weights = weights + alpha * data_matrix.transpose() * error
    return weights


def plotBestFit(w, data, labels):
    weights = w.getA()
    data_arr = np.array(data)
    n = np.shape(data_arr)[0]
    xcord1, ycord1, xcord2, ycord2 = [], [], [], []
    for i in range(n):
        if int(labels[i]) == 1:
            xcord1.append(data_arr[i, 1])
            ycord1.append(data_arr[i, 2])
        else:
            xcord2.append(data_arr[i, 1])
            ycord2.append(data_arr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = np.arange(-3.0, 3.0, 0.1)
    y = (-weights[0] - weights[1] * x) / weights[2]
    ax.plot(x, y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.title('Logistic Regression')
    plt.show()
