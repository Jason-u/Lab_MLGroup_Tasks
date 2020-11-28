#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# 加载MNIST数据集
trainsets = datasets.MNIST('./data', train=True, download=True, transform=transforms.ToTensor())
testsets = datasets.MNIST('./data', train=False, download=True, transform=transforms.ToTensor())

# 查看数据集大小
print(trainsets.data.shape)
print(trainsets.targets.shape)
print(testsets.data.shape)
print(testsets.targets.shape)

# 定义超参数
BATCH_SIZE = 32
EPOCHS = 50

# 创建数据集的可迭代对象
train_loader = torch.utils.data.DataLoader(dataset=trainsets, batch_size=BATCH_SIZE, shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset=testsets, batch_size=BATCH_SIZE, shuffle=True)

# 查看一批数据
images, labels = next(iter(test_loader))
print(images.shape)
print(labels.shape)


# 显示一批数据
def imgshow(inp, title=None):
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])    # 均值
    std = np.array([0.229, 0.224, 0.225])    # 标准差
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)    # 像素值压缩到0-1之间
    plt.imshow(inp)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)


# 网格显示
out = torchvision.utils.make_grid(images)
imgshow(out)


# 定义RNN模型
class RNN_Model(nn.Module):
    def __init__(self, input_dim, hidden_dim, layer_dim, output_dim):
        super(RNN_Model, self).__init__()
        self.hidden_dim = hidden_dim
        self.layer_dim = layer_dim
        self.rnn = nn.RNN(input_dim, hidden_dim, layer_dim, batch_first=True, nonlinearity='relu')
        # 全连接层
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        # 初始化隐层状态全为0
        h0 = torch.zeros(self.layer_dim, x.size(0), self.hidden_dim).requires_grad_().to(device)
        # 分离隐藏状态，避免梯度爆炸
        out, hn = self.rnn(x, h0.detach())
        out = self.fc(out[:, -1, :])
        return out


# 初始化模型
input_dim = 28    # 输入维度
hidden_dim = 100    # 隐层的维度
layer_dim = 2    # 2层RNN
output_dim = 10    # 输出维度
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
model = RNN_Model(input_dim, hidden_dim, layer_dim, output_dim).to(device)

# 定义损失函数（交叉熵损失函数）
criterion = nn.CrossEntropyLoss()

# 定义优化器
learning_rate = 0.01
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

# 输出模型参数信息
print('-' * 85)
print('Parameters Information:')
for i in range(len(list(model.parameters()))):
    print('Parameter %d：' % (i + 1))
    print(list(model.parameters())[i])
    print(list(model.parameters())[i].size())
print('-' * 85)

# 模型训练
sequence_dim = 28    # 序列长度
loss_list = []    # 保存损失的列表
accuracy_list = []    # 保存准确率的列表
iteration_list = []    # 保存循环次数
Iter = 0
print('Training...')
for epoch in range(EPOCHS):
    for i, (images, labels) in enumerate(train_loader):
        model.train()    # 声明训练
        # 将数据转换为RNN的输入维度
        images = images.view(-1, sequence_dim, input_dim).requires_grad_().to(device)
        labels = labels.to(device)
        # 梯度清零，否则会不断累加
        optimizer.zero_grad()
        # 前向传播
        outputs = model(images)
        # 计算损失
        loss = criterion(outputs, labels)
        # 反向传播，更新参数
        loss.backward()
        optimizer.step()
        Iter += 1
        # 模型验证
        if Iter % 500 == 0:
            model.eval()
            # 计算验证的准确率
            correct = 0.0
            total = 0.0
            # 迭代测试集，获取数据，预测
            for images, labels in test_loader:
                # 将数据转换为LSTM的输入维度
                images = images.view(-1, sequence_dim, input_dim).to(device)
                # 模型预测
                outputs = model(images)
                # 获取预测概率最大值的下标
                predict = torch.max(outputs.data, 1)[1]
                # 统计测试集的大小
                total += labels.size(0)
                # 统计预测正确的数量
                if torch.cuda.is_available():
                    correct += (predict.cuda(0) == labels.cuda(0)).sum()
                else:
                    correct += (predict == labels).sum()
            accuracy = correct / total * 100
            loss_list.append(loss.data)
            accuracy_list.append(accuracy)
            iteration_list.append(Iter)
            # 打印信息
            print('Loop    : {}\nLoss    : {}\nAccuracy: {}%'.format(Iter, loss.item(), accuracy))
            print('-' * 55)

# 可视化loss
plt.plot(iteration_list, loss_list)
plt.xlabel('Number of Iteration')
plt.ylabel('Loss')
plt.title('MNIST with RNN')
plt.savefig('./MNIST_with_RNN_Loss.png')
plt.show()

# 可视化accuracy
plt.plot(iteration_list, accuracy_list, color='r')
plt.xlabel('Number of Iteration')
plt.ylabel('Accuracy')
plt.title('MNIST with RNN')
plt.savefig('./MNIST_with_RNN_Accuracy.png')
plt.show()
