import MyApriori


# 加载数据集并打印前10个样本
dataset = [line.strip('\n').split(',') for line in open('./data.txt', encoding='utf-8').readlines()]
for line in dataset[:10]:
    print(line)

# 使用Apriori算法获取关联规则
MyApriori.apriori(dataset=dataset, minSupport=0.0005, minConfidence=0.01)
