from MyDecisionTree_ID3 import *


# 加载数据集
fr = open('./lenses.txt')
lenses = [inst.strip().split('\t') for inst in fr.readlines()]
fr.close()

# 生成ID3决策树
dt = ID3DecisionTree()    # 实例化ID3DecisionTree对象
lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
lensesTree = dt.createTree(lenses, lensesLabels)
print(lensesTree)         # 以字典形式打印决策树

# 生成*.dot文件，实现决策树可视化
with open('./lenses.dot', 'w') as f:
    dot = dt.getDotFileContent(lensesTree)
    f.write(dot)
