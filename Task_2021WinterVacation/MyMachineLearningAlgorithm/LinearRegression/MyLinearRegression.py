"""
MyLinearRegression.py - 基于NumPy实现线性回归
Author: Chen Chunhan
Date  : 2021-1-24
"""
import numpy as np


def lossFunction(w, b, points):
    """
    计算损失函数，这里采用的是MSE
    :param w: 直线斜率
    :param b: 直线截距
    :param points: 样本点集合
    :return: 均方误差值
    """
    loss = 0
    for i in range(len(points)):
        x = points[i, 0]
        y = points[i, 1]
        loss += (y - (w * x + b)) ** 2
    loss /= float(len(points))
    return loss


def stepGrad(w_cur, b_cur, points, lr):
    """
    对w和b进行一次更新
    :param w_cur: 当前的斜率
    :param b_cur: 当前的截距
    :param points: 样本点集合
    :param lr: 学习率
    :return: 更新后的斜率和截距
    """
    w_grad = 0
    b_grad = 0
    for i in range(len(points)):
        x = points[i, 0]
        y = points[i, 1]
        w_grad += (2 / float(len(points))) * ((w_cur * x + b_cur) - y) * x
        b_grad += (2 / float(len(points))) * ((w_cur * x + b_cur) - y)
        w_new = w_cur - (lr * w_grad)
        b_new = b_cur - (lr * b_grad)
    return [w_new, b_new]


def gradientDescent(points, w_start, b_start, lr, num_iterations):
    """
    梯度下降法循环更新w和b
    :param points: 样本点集合
    :param w_start: 初始的斜率
    :param b_start: 初始的截距
    :param lr: 学习率
    :param num_iterations: 迭代次数
    :return: 迭代后的直线斜率和截距
    """
    w = w_start
    b = b_start
    for i in range(num_iterations):
        w, b = stepGrad(w, b, np.array(points), lr)
    return [w, b]
