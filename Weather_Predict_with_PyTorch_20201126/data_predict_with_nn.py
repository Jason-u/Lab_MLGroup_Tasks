#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import datetime
import warnings
import pandas as pd
import numpy as np
from sklearn import preprocessing
import torch
import matplotlib as mpl
import matplotlib.pyplot as plt


warnings.filterwarnings('ignore')

dataset = pd.read_csv('./WeatherData_Processed.csv')
# print('原始数据维度：{0}\n数据：\n{1}'.format(dataset.shape, dataset))

# 对week特征进行One-Hot编码
dataset = pd.get_dummies(dataset)
# print(dataset)

# 指定特征和标签
labels = np.array(dataset['actual'])
features = dataset.drop('actual', axis=1)
feature_list = list(features.columns)    # 单独保存数据集的列名称
features = np.array(features)

input_features = preprocessing.StandardScaler().fit_transform(features)
# print("\n标准化原始数据，维度：{0}\n具体数据：\n{1}".format(input_features.shape, input_features))

# 构建网络模型
input_size = input_features.shape[1]
hidden_size = 128
output_size = 1
batch_size = 16
nn = torch.nn.Sequential(
    torch.nn.Linear(input_size, hidden_size),
    torch.nn.Sigmoid(),
    torch.nn.Linear(hidden_size, output_size)
)
cost = torch.nn.MSELoss(reduction='mean')    # 计算损失函数（均方误差）
optimizer = torch.optim.Adam(nn.parameters(), lr=0.001)    # 优化器

# 训练网络
losses = []
print('Training...')
for i in range(1, 1001):
    batch_loss = []
    # 使用MINI-Batch方法进行训练
    for start in range(0, len(input_features), batch_size):
        end = start + batch_size if start + batch_size < len(input_features) else len(input_features)
        xx = torch.tensor(input_features[start:end], dtype=torch.float, requires_grad=True)
        yy = torch.tensor(labels[start:end], dtype=torch.float, requires_grad=True)
        prediction = nn(xx)
        loss = cost(prediction, yy)
        optimizer.zero_grad()
        loss.backward(retain_graph=True)
        # 所有optimizer都实现了step()方法，它会更新所有的参数
        # 一旦梯度被如backward()之类的函数计算好后，我们就可以调用这个函数
        optimizer.step()
        batch_loss.append(loss.data.numpy())
    # 打印损失，每100轮打印一次
    if i % 100 == 0:
        losses.append(np.mean(batch_loss))
        print('Epoch: {0:<5d}Loss: {1}\n{2}'.format(i, np.mean(batch_loss), batch_loss))

# 预测训练结果
x = torch.tensor(input_features, dtype=torch.float)
predict = nn(x).data.numpy()

# 转换日期格式
months = features[:, feature_list.index('month')]
days = features[:, feature_list.index('day')]
years = features[:, feature_list.index('year')]
dates = [str(int(year)) + '-' + str(int(month)) + '-' + str(int(day)) for year, month, day in zip(years, months, days)]
dates = [datetime.datetime.strptime(date, '%Y-%m-%d') for date in dates]

# 创建一个数据框来存日期和其对应的标签数值
true_data = pd.DataFrame(data={'date': dates, 'actual': labels})

# 再创建一个数据框来存日期和其对应的模型预测值
test_dates = [str(int(year)) + '-' + str(int(month)) + '-' + str(int(day)) for year, month, day in
              zip(years, months, days)]
test_dates = [datetime.datetime.strptime(date, '%Y-%m-%d') for date in test_dates]
predictions_data = pd.DataFrame(data={'date': test_dates, 'prediction': predict.reshape(-1)})

# 绘图
mpl.rcParams["font.sans-serif"] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False
plt.plot(true_data['date'], true_data['actual'], 'b+', label='真实值')
plt.plot(predictions_data['date'], predictions_data['prediction'], 'r+', label='预测值')
plt.xticks(rotation='60')
plt.legend()
plt.xlabel('日期')
plt.ylabel('最高温度')
plt.title('真实温度&预测温度')
plt.show()
