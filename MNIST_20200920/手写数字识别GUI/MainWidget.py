#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.Qt import QWidget, QColor, QPixmap, QIcon, QSize, QCheckBox
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QSplitter, QComboBox, QLabel, QSpinBox, QFileDialog
import keras
import numpy as np
from PaintBoard import PaintBoard


class MainWidget(QWidget):
    def __init__(self, Parent=None):
        """
        Constructor
        """
        super().__init__(Parent)
        self.__InitData()  # 先初始化数据，再初始化界面
        self.__InitView()

    def __InitData(self):
        """
        初始化成员变量
        """
        self.__paintBoard = PaintBoard(self)
        # 获取颜色列表(字符串类型)
        self.__colorList = QColor.colorNames()

    def __InitView(self):
        """
        初始化界面
        """
        self.setFixedSize(640, 480)
        self.setWindowTitle("手写数字识别 v2.1")
        # 新建一个水平布局作为本窗体的主布局
        main_layout = QHBoxLayout(self)
        # 设置主布局内边距以及控件间距为10px
        main_layout.setSpacing(10)
        # 在主界面左侧放置画板
        main_layout.addWidget(self.__paintBoard)
        # 新建垂直子布局用于放置按键
        sub_layout = QVBoxLayout()
        # 设置此子布局和内部控件的间距为10px
        sub_layout.setContentsMargins(10, 10, 10, 10)
        self.__btn_Clear = QPushButton("清空画板")
        self.__btn_Clear.setParent(self)  # 设置父对象为本界面
        # 将按键按下信号与画板清空函数相关联
        self.__btn_Clear.clicked.connect(self.__paintBoard.Clear)
        sub_layout.addWidget(self.__btn_Clear)
        self.__btn_Quit = QPushButton("退出")
        self.__btn_Quit.setParent(self)  # 设置父对象为本界面
        self.__btn_Quit.clicked.connect(self.Quit)
        sub_layout.addWidget(self.__btn_Quit)
        self.__cbtn_Eraser = QCheckBox("  使用橡皮擦")
        self.__cbtn_Eraser.setParent(self)
        self.__cbtn_Eraser.clicked.connect(self.on_cbtn_Eraser_clicked)
        sub_layout.addWidget(self.__cbtn_Eraser)
        splitter = QSplitter(self)  # 占位符
        sub_layout.addWidget(splitter)
        self.__btn_Recognize = QPushButton("开始识别")
        self.__btn_Recognize.setParent(self)
        self.__btn_Recognize.clicked.connect(self.on_btn_Recognize_Clicked)
        sub_layout.addWidget(self.__btn_Recognize)
        self.__label_penThickness = QLabel(self)
        self.__label_penThickness.setText("画笔粗细")
        self.__label_penThickness.setFixedHeight(20)
        sub_layout.addWidget(self.__label_penThickness)
        self.__spinBox_penThickness = QSpinBox(self)
        self.__spinBox_penThickness.setMaximum(45)
        self.__spinBox_penThickness.setMinimum(20)
        self.__spinBox_penThickness.setValue(45)  # 默认粗细为45
        self.__spinBox_penThickness.setSingleStep(1)  # 最小变化值为2
        self.__spinBox_penThickness.valueChanged.connect(
            self.on_PenThicknessChange)  # 关联spinBox值变化信号和函数on_PenThicknessChange
        sub_layout.addWidget(self.__spinBox_penThickness)
        self.__label_penColor = QLabel(self)
        self.__label_penColor.setText("画笔颜色")
        self.__label_penColor.setFixedHeight(20)
        sub_layout.addWidget(self.__label_penColor)
        self.__comboBox_penColor = QComboBox(self)
        self.__fillColorList(self.__comboBox_penColor)  # 用各种颜色填充下拉列表
        self.__comboBox_penColor.currentIndexChanged.connect(
            self.on_PenColorChange)  # 关联下拉列表的当前索引变更信号与函数on_PenColorChange
        sub_layout.addWidget(self.__comboBox_penColor)
        main_layout.addLayout(sub_layout)  # 将子布局加入主布局

    def __fillColorList(self, comboBox):
        index_black = 0
        index = 0
        for color in self.__colorList:
            if color == "white":
                index_black = index
            index += 1
            pix = QPixmap(70, 20)
            pix.fill(QColor(color))
            comboBox.addItem(QIcon(pix), None)
            comboBox.setIconSize(QSize(70, 20))
            comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        comboBox.setCurrentIndex(index_black)

    def on_PenColorChange(self):
        color_index = self.__comboBox_penColor.currentIndex()
        color_str = self.__colorList[color_index]
        self.__paintBoard.ChangePenColor(color_str)

    def on_PenThicknessChange(self):
        penThickness = self.__spinBox_penThickness.value()
        self.__paintBoard.ChangePenThickness(penThickness)

    def on_cbtn_Eraser_clicked(self):
        if self.__cbtn_Eraser.isChecked():
            self.__paintBoard.EraserMode = True   # 进入橡皮擦模式
        else:
            self.__paintBoard.EraserMode = False  # 退出橡皮擦模式

    def on_btn_Recognize_Clicked(self):
        savePath = './keras_MNIST_test_imgs/GUI_test_img.png'
        image = self.__paintBoard.GetContentAsQImage()
        image.save(savePath)
        # print(savePath)
        network = keras.models.load_model('./MNIST_model.h5')
        # 加载图像
        mnist_test_img = keras.preprocessing.image.load_img(savePath, target_size=(28, 28))
        mnist_test_img = mnist_test_img.convert('L')

        # 对手写数字进行识别
        def find_nearest(array, value):
            array = np.asarray(array)
            return (np.abs(array - value)).argmin()

        def find_second(array, value):
            array = np.asarray(array)
            array[find_nearest(array, 1)] = 0
            return find_nearest(array, 1)

        mnist_test_img = mnist_test_img.convert('L')
        img_data = list(mnist_test_img.getdata())
        test_img_data = np.array([255 - (255 - x) * 1.0 for x in img_data]) \
            .reshape((1, 28 * 28)).astype(float)
        y_pre = network.predict(test_img_data)
        result1 = find_nearest(y_pre[0], 1)
        result1_probability = y_pre[0][result1] * 100
        result2 = find_second(y_pre[0], 1)
        result2_probability = y_pre[0][result2] * 100
        print('---------------------------------------------------------------------------')
        print('识别结果：\nFirst  guess: %-3dProbability: %-.2f%%' % (result1, result1_probability))
        print('Second guess: %-3dProbability: %-.2f%%' % (result2, result2_probability))
        print('---------------------------------------------------------------------------')

    def Quit(self):
        self.close()
