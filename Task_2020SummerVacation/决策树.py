#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor


# 加载数据集
dataset = pd.read_csv('LabeledTianjinRentHouseInfo.csv', encoding='gbk')

# 使用train_test_split()分离出测试集和训练集
X_train, X_test, y_train, y_test = train_test_split(np.array(dataset.drop(columns=['月租'])), np.array(dataset['月租']),
                                                    test_size=0.25, random_state=22)
print(y_test)

# 构建决策树模型
dtr = DecisionTreeRegressor()
dtr.fit(X_train, y_train)
y_pred = dtr.predict(X_test)
print(y_pred)
print('Training set score: {:.2f}'.format(dtr.score(X_train, y_train)))
print('Test set score: {:.2f}'.format(dtr.score(X_test, y_test)))
