"""
MyKMeans.py - 基于NumPy实现KMeans聚类算法
Author: Chen Chunhan
Date  : 2021-1-21

K-means算法以k为参数，把n个对象分成k个簇，使簇内具有较高的相似度，而簇间的相似度较低。
处理过程：
    1.随机选择k个点作为初始的聚类中心。
    2.对于剩下的点，根据其与聚类中心的距离，将其归入最近的簇。
    3.对每个簇，计算所有点的均值作为新的聚类中心。
    4.重复步骤2、3直到聚类中心不再发生改变。
"""
import numpy as np


def InitializeCentroids(points, k):
    """
    KMeans聚类算法初始化，随机选择k个点作为初始的聚类中心
    :param points: 样本集
    :param k: 聚类簇数
    :return: 随机选择的k个聚类中心
    """
    centroids = points.copy()
    np.random.shuffle(centroids)
    return centroids[:k]


def ClosestCentroid(points, centroids):
    """
    计算每个样本与聚类中心的欧式距离，将其归入最近的簇
    :param points: 样本集
    :param centroids: 聚类中心
    :return: 样本所属聚类的簇
    """
    euclDist = np.sqrt(((points - centroids[:, np.newaxis]) ** 2).sum(axis=2))
    return np.argmin(euclDist, axis=0)


def UpdateCentroids(points, closestCentroid, centroids):
    """
    对每个簇计算所有点的均值作为新的聚类中心
    :param points: 样本集
    :param closestCentroid:
    :param centroids: 上一轮迭代的聚类中心
    :return: 新的聚类中心
    """
    return np.array([points[closestCentroid == k].mean(axis=0) for k in range(centroids.shape[0])])


def KMeans(points, k=3, maxIters=10):
    """
    KMeans聚类算法实现
    :param points: 样本集
    :param k: 聚类簇数
    :param maxIters: 最大迭代次数
    :return: 聚类后的簇划分
    """
    centroids = InitializeCentroids(points=points, k=k)
    for i in range(maxIters):
        closestCentroid = ClosestCentroid(points=points, centroids=centroids)
        newCentroids = UpdateCentroids(points=points, closestCentroid=closestCentroid, centroids=centroids)
        if (newCentroids == centroids).all():    # 聚类中心不再发生改变，停止迭代
            break
        centroids = newCentroids
    return centroids, closestCentroid, points
