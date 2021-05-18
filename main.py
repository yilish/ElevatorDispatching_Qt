# -*- coding: utf-8 -*-
# @Time    : 2021/05/18
# @Author  : Yili Shen
# @Email   : 1851009@tongji.edu.cn
# @File    : main.py
# @Software: PyCharm Python3.9 MacOS 10.15.3

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import mainwindowui


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()

    ui = mainwindowui.MainWindowUI()
    ui.initUI(MainWindow)
    t_arr = []
    for i in range (len(ui.elevator_arr)):

        t = mainwindowui.MyThread(ui.elevator_arr[i])
        t.start()
        t_arr.append(t)
    # ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())