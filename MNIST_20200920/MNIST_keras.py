#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from keras.utils import to_categorical
from keras import models, layers, regularizers
from keras.optimizers import RMSprop
from keras.datasets import mnist
# import matplotlib.pyplot as plt

# 加载数据集
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
# print(train_images.shape, test_images.shape)
# print(train_images[0])
# print(train_labels[0])
# plt.imshow(train_images[0])
# plt.show()

# 数据预处理
train_images = train_images.reshape((60000, 28 * 28)).astype('float')
test_images = test_images.reshape((10000, 28 * 28)).astype('float')
# One-Hot编码
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)
# print(train_labels[0])

# 搭建一个神经网络
network = models.Sequential()
# 全连接层
# 正则化防止过拟合
network.add(layers.Dense(units=128, activation='relu', input_shape=(28 * 28,),
                         kernel_regularizer=regularizers.l1(0.0001)))
network.add(layers.Dropout(0.01))
network.add(layers.Dense(units=32, activation='relu',
                         kernel_regularizer=regularizers.l1(0.0001)))
network.add(layers.Dropout(0.01))
# 输出层
network.add(layers.Dense(units=10, activation='softmax'))
# print(network.summary())

# 神经网络训练
# 编译：确定优化器和损失函数等
network.compile(optimizer=RMSprop(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
# 训练网络：确定训练的数据、训练的轮数和每次训练的样本数等
# 用fit()函数，epochs表示训练多少个回合，batch_size表示每次训练给多大的数据
network.fit(train_images, train_labels, epochs=20, batch_size=128, verbose=2)

# 用训练好的模型进行预测，并在测试集上做出评价
# y_pre = network.predict(test_images[:5])
# print(y_pre, test_labels[:5])
test_loss, test_accuracy = network.evaluate(test_images, test_labels)
print('test_loss: ', test_loss, '    test_accuracy', test_accuracy)
