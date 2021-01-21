"""
MyDecisionTree.py - 基于NumPy实现ID3决策树算法
Author: Chen Chunhan
Date  : 2021-1-22

ID3决策树学习算法以信息增益为准则来选择划分属性。
已知一个随机变量的信息后使得另一个随机变量的不确定性减小的程度叫做信息增益，
即信息增益越大，使用该属性来进行划分所获得的纯度提升越大。
"""
from collections import namedtuple
import operator
import uuid

import numpy as np


class ID3DecisionTree():
    def __init__(self):
        self.tree = {}
        self.dataset = []
        self.labels = []

    def InformationEntropy(self, dataset):
        """
        计算信息熵
        :param dataset: 样本集合
        :return: 信息熵
        """
        labelCounts = {}
        for featureVector in dataset:
            currentLabel = featureVector[-1]    # 从数据集中得到类别标签
            if currentLabel not in labelCounts.keys():
                labelCounts[currentLabel] = 0
            labelCounts[currentLabel] += 1
        ent = 0.0
        for key in labelCounts:
            prob = float(labelCounts[key]) / len(dataset)
            ent -= prob * np.log2(prob)
        return ent

    def splitDataset(self, dataset, axis, value):
        """
        按照给定特征划分数据集
        :param dataset: 待划分的数据集
        :param axis: 划分数据集的特征
        :param value: 特征的返回值
        :return: 划分后的数据集
        """
        retDataset = []
        for featureVector in dataset:
            if featureVector[axis] == value:
                reducedFeatureVector = featureVector[:axis]
                reducedFeatureVector.extend(featureVector[axis + 1:])
                retDataset.append(reducedFeatureVector)
        return retDataset

    def chooseBestFeatureToSplit(self, dataset):
        """
        选择最好的数据集划分方式
        :param dataset: 待划分的数据集
        :return: 最好的划分数据集的特征
        """
        numFeatures = len(dataset[0]) - 1    # 计算特征向量维数，其中最后一列用于类别标签，因此要减去
        baseEntropy = self.InformationEntropy(dataset)
        bestInfoGain = 0.0
        bestFeature = -1
        for i in range(numFeatures):         # 遍历数据集各列，计算最优特征轴
            featureList = [example[i] for example in dataset]
            uniqueValues = set(featureList)
            newEntropy = 0.0
            for value in uniqueValues:       # 按列和唯一值计算信息熵
                subDataset = self.splitDataset(dataset, i, value)    # 按指定列i和唯一值分隔数据集
                prob = len(subDataset) / float(len(dataset))
                newEntropy += prob * self.InformationEntropy(subDataset)
            infoGain = baseEntropy - newEntropy
            if infoGain > bestInfoGain:
                bestInfoGain = infoGain      # 用当前信息增益值替代之前的最优增益值
                bestFeature = i              # 重置最优特征为当前列
        return bestFeature

    def majorityCount(self, classList):
        """
        如果数据集已经处理了所有属性但类标签仍不唯一，采用多数表决的方法决定叶子结点的分类
        :param classList: 分类列表
        :return: 叶子结点的分类
        """
        classCount = {}
        for vote in classList:
            if vote not in classCount.keys():
                classCount[vote] = 0
            classCount[vote] += 1
        sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sortedClassCount[0][0]

    def createTree(self, dataset, labels):
        """
        构造ID3决策树
        :param dataset: 数据集
        :param labels: 特征
        :return: 字典形式的ID3决策树
        """
        classList = [example[-1] for example in dataset]
        # 递归返回情形1，classList只有一种决策标签，停止划分，返回这个决策标签
        if classList.count(classList[0]) == len(classList):
            return classList[0]
        # 递归返回情形2，数据集的第一个决策标签只有一个，停止划分，返回这个决策标签
        if len(dataset[0]) == 1:
            return self.majorityCount(classList)
        bestFeature = self.chooseBestFeatureToSplit(dataset)
        bestFeatureLabel = labels[bestFeature]
        tree = {bestFeatureLabel: {}}
        del labels[bestFeature]
        featureValues = [example[bestFeature] for example in dataset]
        uniqueValues = set(featureValues)
        # 决策树递归生长，将删除后的特征类别集建立子类别集，按最优特征列和值划分数据集，构建子树
        for value in uniqueValues:
            subLabels = labels[:]
            tree[bestFeatureLabel][value] = self.createTree(self.splitDataset(dataset, bestFeature, value), subLabels)
        return tree

    def getNodesAndEdges(self, tree=None, root_node=None):
        """
        递归获取树的结点和边
        :param tree: 要进行可视化的决策树
        :param root_node: 树的根结点
        :return: 树的结点集和边集
        """
        Node = namedtuple('Node', ['id', 'label'])
        Edge = namedtuple('Edge', ['start', 'end', 'label'])
        if tree is None:
            tree = self.tree
        if type(tree) is not dict:
            return [], []
        nodes, edges = [], []
        if root_node is None:
            label = list(tree.keys())[0]
            root_node = Node._make([uuid.uuid4(), label])
            nodes.append(root_node)
        for edge_label, sub_tree in tree[root_node.label].items():
            node_label = list(sub_tree.keys())[0] if type(sub_tree) is dict else sub_tree
            sub_node = Node._make([uuid.uuid4(), node_label])
            nodes.append(sub_node)
            edge = Edge._make([root_node, sub_node, edge_label])
            edges.append(edge)
            sub_nodes, sub_edges = self.getNodesAndEdges(sub_tree, root_node=sub_node)
            nodes.extend(sub_nodes)
            edges.extend(sub_edges)
        return nodes, edges

    def getDotFileContent(self, tree):
        """
        生成*.dot文件，以便可视化决策树
        :param tree: 待可视化的决策树
        :return: *.dot文件的文本
        """
        content = 'digraph decision_tree {\n'
        nodes, edges = self.getNodesAndEdges(tree)
        for node in nodes:
            content += ' "{}" [label="{}"];\n'.format(node.id, node.label)
        for edge in edges:
            start, label, end = edge.start, edge.label, edge.end
            content += ' "{}" -> "{}" [label="{}"];\n'.format(start.id, end.id, label)
        content += '}'
        return content
