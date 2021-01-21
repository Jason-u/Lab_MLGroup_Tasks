import matplotlib.pyplot as plt
import numpy as np

import MyKMeans


# 加载数据集
data = np.loadtxt('./dataset.txt')
plt.scatter(data[:, :1], data[:, 1:2])
plt.xlabel('x')
plt.ylabel('y')
plt.title('Raw Data')
plt.savefig('./RawData.jpg')
plt.show()

# KMeans聚类
k = 3
centroids, closestCentroid, points = MyKMeans.KMeans(data, k, 10)

# 可视化
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
markers = ['+', 'x', 's', 'p', 'o', '^', 'v', '.']
for i in range(k):
    cluster = []
    clusterCenter = plt.scatter(centroids[i:i + 1, :1], centroids[i:i + 1, 1:], s=150, c=colors[i], marker='*',
                                label='Cluster Center {}'.format(i + 1))
    for j in range(len(closestCentroid)):
        if closestCentroid[j] == i:
            cluster.append(points[j])
    cluster = np.array(cluster)
    plt.scatter(cluster[:, :1], cluster[:, 1:], s=50, c=colors[i], marker=markers[i], label='Cluster {}'.format(i + 1))
plt.legend(loc='best')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Data Clustering by K-Means')
plt.savefig('./DataClusteringByKMeans.jpg')
plt.show()
