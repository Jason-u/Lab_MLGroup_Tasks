import matplotlib.pyplot as plt
import numpy as np

import MyLinearRegression


# 随机生成线性数据集
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.rand(100, 1)
points = []
for i in range(len(X)):
    points.append([X[i, 0], y[i, 0]])
print('The actual linear model is: y = 3x + 4')

# 线性回归及可视化
plt.scatter(X, y)
plt.title('Linear Regression')
w_init = 0
b_init = 0
num_iterations = 0
colors = ['b', 'g', 'y', 'c', 'm', 'r']
i = 0
loss_list = []
while num_iterations <= 1000:
    [w, b] = MyLinearRegression.gradientDescent(points, w_init, b_init, lr=0.01, num_iterations=num_iterations)
    loss = MyLinearRegression.lossFunction(w, b, np.array(points))
    loss_list.append(loss)
    print('After {:<4d} iterations: y = {:<8.6f}x + {:<8.6f}  Loss: {}'.format(num_iterations, w, b, loss))
    X_line = np.arange(-0.1, 2.2, 0.1)
    y_line = w * X_line + b
    plt.plot(X_line, y_line, c=colors[i], label='After {} iterations'.format(num_iterations))
    num_iterations += 200
    i += 1
plt.legend(loc='best')
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('./LinearRegression.jpg')
plt.show()

# 绘制损失曲线
plt.plot([i for i in range(1001) if i % 200 == 0 and i != 0], loss_list[1:])
plt.title('MSE Loss')
plt.xlabel('Iterations')
plt.ylabel('Loss')
plt.savefig('./LinearRegressionLoss.jpg')
plt.show()
