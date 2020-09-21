#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
import os
import scipy.misc
import tensorflow.compat.v1 as tf


tf.disable_v2_behavior()


mnist = input_data.read_data_sets('./mnist', one_hot=True)
# print(mnist.train.images.shape)
# print(mnist.train.labels.shape)
# print(mnist.train.images[0, :])
# print(mnist.train.labels[0, :])
#
# dir_data = './mnist/raw/'
# if os.path.exists(dir_data) is False:
#     os.makedirs(dir_data)
#
# for i in range(5):
#     image_array = mnist.train.images[i, :]
#     image_array = image_array.reshape(28, 28)
#     image_file = dir_data + 'mnist_train_%d.jpg' % i
#     scipy.misc.toimage(image_array, cmin=0.0, cmax=1.0).save(image_file)
#     image_label = mnist.train.labels[i, :]
#     label = np.argmax(image_label)
#     print('image_train_%d  label: %d' % (i, label))

x = tf.placeholder(tf.float32, [None, 784])
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
y_ = tf.placeholder(tf.float32, [None, 10])

# y = softmax(x * W + b)
y = tf.nn.softmax(tf.matmul(x, W) + b)

# 构建损失函数（交叉熵损失函数）
cross_entrpy = tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entrpy)

with tf.Session() as sess:
    tf.global_variables_initializer().run()
    for _ in range(1000):
        batch_xs, batch_ys = mnist.train.next_batch(100)
        sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

    curr_pre = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    acc = tf.reduce_mean(tf.cast(curr_pre, tf.float32))
    print(sess.run(acc, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
