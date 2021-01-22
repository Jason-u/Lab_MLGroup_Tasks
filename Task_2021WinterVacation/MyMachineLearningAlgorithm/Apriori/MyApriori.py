"""
MyApriori.py - 实现Apriori算法
Author: Chen Chunhan
Date  : 2021-1-22
"""
import itertools


def createC1(dataset):
    """
    生成候选1项集列表
    :param dataset: 数据集
    :return: 候选1项集列表
    """
    item1 = set(itertools.chain(*dataset))
    return [frozenset(i) for i in item1]


def C2L(dataset, Ck, minSupport):
    """
    根据候选k项集和对应的最小支持度生成频繁k项集
    :param dataset: 数据集
    :param Ck: 候选k项集
    :param minSupport: 最小支持度
    :return: 频繁k项集
    """
    support = {}
    for row in dataset:
        for item in Ck:
            if item.issubset(row):
                support[item] = support.get(item, 0) + 1
    total = len(dataset)
    return {key: val / total for key, val in support.items() if val / total >= minSupport}


def L2C(LkList):
    """
    由频繁k项集组合生成候选k+1项集
    :param LkList: 所有频繁k项集构成的列表
    :return: 所有候选k+1项集构成的集合
    """
    C = set()
    LkSize = len(LkList)
    if LkSize > 1:                       # 如果频繁k项集的数量不大于1，不再生成候选k+1项集
        k = len(LkList[0])               # 获取k值
        for i, j in itertools.combinations(range(LkSize), 2):
            t = LkList[i] | LkList[j]    # 对两个频繁k项集进行组合生成新的集合t
            if len(t) == k + 1:          # 如果t是k+1项集，加入到C中
                C.add(t)
    return C


def getAllL(dataset, minSupport):
    """
    根据最小支持度从数据集中获取所有频繁项集
    :param dataset: 数据集
    :param minSupport: 最小支持度
    :return: 所有频繁项集构成的字典
    """
    C1 = createC1(dataset)
    L1 = C2L(dataset, C1, minSupport)
    allL = L1
    Lk = L1
    while len(Lk) > 1:
        LkKeyList = list(Lk.keys())
        C = L2C(LkKeyList)
        Lk = C2L(dataset, C, minSupport)
        if len(Lk) > 0:
            allL.update(Lk)
        else:
            break
    return allL


def generateRules(item):
    """
    根据频繁项集生成关联规则
    :param item: 频繁项集
    :return: 所有关联规则组合
    """
    left = []
    for i in range(1, len(item)):
        left.extend(itertools.combinations(item, i))
    return [(frozenset(le), frozenset(item.difference(le))) for le in left]


def allRules(allL, minConfidence):
    """
    从所有频繁项集字典中生成关联规则列表
    :param allL: 所有频繁项集
    :param minConfidence: 最小置信度
    :return: 所有满足最小置信度的关联规则
    """
    rules = []
    for Lk in allL:
        if len(Lk) > 1:
            rules.extend(generateRules(Lk))
    res = []
    for left, right in rules:
        support = allL[left | right]
        confidence = support / allL[left]
        lift = confidence / allL[right]
        if confidence >= minConfidence:
            res.append({'左侧': left, '右侧': right, '支持度': support, '置信度': confidence, '提升度': lift})
            print('{}->{} 支持度：{} 置信度：{} 提升度：{}'.format(left, right, support, confidence, lift))
    return res


def apriori(dataset, minSupport, minConfidence):
    """
    找出数据集中满足最小支持度和最小置信度的所有关联规则
    :param dataset: 数据集
    :param minSupport: 最小支持度
    :param minConfidence: 最小置信度
    :return: 所有满足条件的关联规则
    """
    allL = getAllL(dataset, minSupport)
    return allRules(allL, minConfidence)
