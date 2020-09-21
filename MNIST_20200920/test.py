#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from tensorflow.examples.tutorials.mnist import input_data

# 载入MNIST数据集，如果指定地址下没有下载好的数据，那么TensorFlow会自动在网站上下载数据
mnist = input_data.read_data_sets("E:/Tensorflow_GPU_PyCharm/MNIST/mnist")

# 打印训练数据大小
print("Training data size:", mnist.train.num_examples)

# 打印验证集大小
print("Validating data size:", mnist.validation.num_examples)

# 打印测试集大小
print("Testing data size:", mnist.test.num_examples)

# 打印训练样例
print("Example training data", mnist.train.images[0])

# 打印训练样例的标签
print("Example training data label:", mnist.train.labels[0])
