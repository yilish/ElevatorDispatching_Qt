# -*- coding: utf-8 -*-
# @Time    : 2021/05/18
# @Author  : Yili Shen
# @Email   : 1851009@tongji.edu.cn
# @File    : mainwindowui.py
# @Software: PyCharm Python3.9 MacOS 10.15.3


import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLCDNumber, QPushButton
from PyQt5 import QtCore, QtGui
from functools import partial
from PyQt5.QtCore import QThread
import dispatch_thread
import time
import random


class elevator(QWidget):
    def __init__(self):
        super(elevator, self).__init__()
        self.button_arr = []
        self.target_list = []
        self.up_flag = 1
        self.target = 15
        self.is_moving = 0

    def set_right_floor(self, right):
        self.right_floor = right

    def set_target(self, para: QPushButton):
        s = para.text()
        num = int(s)
        if not para.isChecked():
            if num in self.target_list:
                self.target_list.remove(num)
            print(self.target_list)
            return

        if num not in self.target_list:
            self.target_list.append(num)
        print(self.target_list)

    def elevator_move(self, target):
        num = self.lcd.intValue()
        print(num)

    def init_elevator(self, mw, x, y):
        # LCD generation
        self.lcd = QLCDNumber(mw)
        self.lcd.resize(95, 50)
        self.lcd.move(x, y)
        self.lcd.display('1')
        # for each button: h = 30,
        # w = 50, x = 60 * i % 2,
        # y = 110 + 35 * i / 2
        # button generation
        for i in range(20):
            tmp_button = QPushButton(mw)
            tmp_button.setGeometry(x + 45 * (i % 2), y + 50 + 35 * (int(i / 2)), 55, 35)
            tmp_button.setText(str(20 - i))
            tmp_button.clicked.connect(partial(self.set_target, tmp_button))
            # tmp_button.clicked.connect(partial(self.check_floor, 20 - i))
            tmp_button.setCheckable(True)
            self.button_arr.append(tmp_button)

        # initialization of check button
        self.btn_pause = QPushButton(mw)
        self.btn_pause.setGeometry(x, y + 400, 100, 50)
        self.btn_pause.setText('暂停')
        #        self.btn_pause.clicked.connect(partial(self.elevator_move, 10))
        self.btn_pause.setCheckable(True)
        # initialization of open label
        self.lbl_open = QLabel(mw)
        self.lbl_open.setGeometry(x, y + 450, 100, 50)
        self.lbl_open.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_open.setStyleSheet(
            'QLabel {background-color: #ffffff; color: blue;border-width: 10;border-color: red;}')
        self.lbl_open.setText('Open')
        self.lbl_open.hide()
        print(len(self.button_arr))


class MyThread(QThread):
    def __init__(self, elev: elevator):
        super().__init__()
        self.elev = elev
        # self.elevator_move(5)
        self.up_queue = []
        self.down_queue = []

    def run(self) -> None:
        while 1:
            self.elev.lbl_open.hide()
            if self.elev.btn_pause.isChecked():
                time.sleep(1)
                continue
            num = self.elev.lcd.intValue()
            if len(self.elev.target_list) == 0:
                self.elev.is_moving = 0
                self.elev.right_floor.flr_up_btn_arr[20 - num].setChecked(False)
                self.elev.right_floor.flr_down_btn_arr[20 - num].setChecked(False)
                time.sleep(1)
                continue
            if not self.elev.is_moving:  # 此时电梯没在动
                # 那么就检查楼层按动的先后顺序吧
                target = self.elev.target_list[0]

                if target >= num:
                    self.elev.up_flag = 1
                else:
                    self.elev.up_flag = 0

                if target == num:
                    self.elev.target_list.remove(num)
                    # self.up_queue.remove(num)
                    self.elev.lbl_open.show()
                    self.elev.button_arr[20 - num].setChecked(False)
                    self.elev.right_floor.flr_up_btn_arr[20 - num].setChecked(False)
                    self.elev.right_floor.flr_down_btn_arr[20 - num].setChecked(False)
                else:
                    self.elev.lcd.display(str(num + 1))
                self.elev.is_moving = 1

            # 电梯在动
            if self.elev.up_flag == 1:
                self.up_queue = list(filter(lambda x: x >= num, self.elev.target_list))
                if len(self.up_queue) == 0:
                    self.elev.is_moving = 0
                    time.sleep(1)
                    self.elev.right_floor.flr_up_btn_arr[20 - num].setChecked(False)
                    # if len(self.down_queue) == 0:

                    continue
                target = min(self.up_queue)
                if target == num:
                    self.elev.target_list.remove(num)
                    self.up_queue.remove(num)
                    self.elev.lbl_open.show()
                    self.elev.button_arr[20 - num].setChecked(False)
                    self.elev.right_floor.flr_up_btn_arr[20- num].setChecked(False)
                else:
                    self.elev.is_moving = 1
                    self.elev.lcd.display(str(num + 1))
            # 下行中
            else:
                self.down_queue = list(filter(lambda x: x <= num, self.elev.target_list))
                # self.up_queue = list(filter(lambda x: x >= num, self.elev.target_list))
                if len(self.down_queue) == 0:
                    self.elev.is_moving = 0
                    self.elev.right_floor.flr_down_btn_arr[20 - num].setChecked(False)
                    time.sleep(1)
                    # if len(self.down_queue) == 0:
                    #     self.elev.is_moving = 0
                    continue
                target = max(self.down_queue)
                if target == num:
                    self.elev.target_list.remove(num)
                    self.down_queue.remove(num)
                    self.elev.lbl_open.show()
                    self.elev.button_arr[20 - num].setChecked(False)
                    self.elev.right_floor.flr_down_btn_arr[20- num].setChecked(False)
                else:
                    self.elev.is_moving = 1
                    self.elev.lcd.display(str(num - 1))
            time.sleep(1)




class floor_btn(QWidget):

    def __init__(self, elev_arr):
        super(floor_btn, self).__init__()

        self.flr_up_btn_arr = []
        self.flr_down_btn_arr = []
        self.elev_arr = elev_arr


    def init_floorbtn(self, mw):
        for i in range(20):
            tmp_button1 = QPushButton(mw)
            tmp_button1.setGeometry(505, 24 * i, 40, 20)
            tmp_button1.setText('{0}⬆️'.format(20 - i))
            tmp_button1.setObjectName('{0}up'.format(20 - i))
            font = QtGui.QFont()
            font.setFamily("Arial")  # 括号里可以设置成自己想要的其它字体
            font.setPointSize(8)
            tmp_button1.setFont(font)
            tmp_button1.clicked.connect(partial(self.decide_which_elevator, tmp_button1))
            tmp_button1.setCheckable(True)
            tmp_button2 = QPushButton(mw)
            tmp_button2.setGeometry(540, 24 * i, 40, 20)
            tmp_button2.setStyleSheet("QPushButton{border-width: 20px;}")
            tmp_button2.setText('{0}⬇️'.format(20 - i))
            tmp_button2.setFont(font)
            tmp_button2.setObjectName('{0}down'.format(20 - i))
            tmp_button2.clicked.connect(partial(self.decide_which_elevator, tmp_button2))
            tmp_button2.setCheckable(True)
            self.flr_up_btn_arr.append(tmp_button1)
            self.flr_down_btn_arr.append(tmp_button2)

    def decide_which_elevator(self, but: QPushButton):
        # 在此处，若电梯静止或者行动方向与电梯方向一致，则取abs
        # 若不一致，电梯上行、按钮下行则取20 - ele_num + 20 - num
        # 电梯下行、按钮上行则取ele_num + num
        if not but.isChecked():
            but.setChecked(True)
            return
        name = but.objectName()
        try:
            num = int(name[:2])
        except:
            num = int(name[0])
        this_up_flag = 0
        if name[-2:] == 'up':
            this_up_flag = 1
        minVal = 2e9
        minIdx = -1
        for i in range(len(self.elev_arr)):
            val = 0
            ele_num = self.elev_arr[i].lcd.intValue()
            if not self.elev_arr[i].is_moving:
                val = abs(num - ele_num)
            else:
                if self.elev_arr[i].up_flag == this_up_flag:
                    val = abs(num - ele_num)
                else:
                    if this_up_flag == 1:
                        val = 40 - ele_num - num
                    else:
                        val = ele_num + num
            if minVal > val:
                minIdx = i
                minVal = val
        if num not in self.elev_arr[minIdx].target_list:
            self.elev_arr[minIdx].target_list.append(num)

class MainWindowUI(QWidget):

    def __init__(self):
        super(MainWindowUI, self).__init__()
        self.elevator_arr = []

    def initUI(self, mw):
        # self.create_one_elevator(0, 0, mw)
        mw.resize(600, 500)

        for i in range(5):
            x = 100 * i
            tmp_elevator = elevator()
            tmp_elevator.init_elevator(mw, x, 0)
            self.elevator_arr.append(tmp_elevator)

        btn_right = floor_btn(self.elevator_arr)
        btn_right.init_floorbtn(mw)
        for i in range(5):
            self.elevator_arr[i].set_right_floor(btn_right)
