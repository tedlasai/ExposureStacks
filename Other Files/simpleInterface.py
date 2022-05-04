from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QComboBox)
from PyQt5.QtGui import QPixmap
import os

from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Control2 import Control

aperture_data = ['F4.0', 'F4.5', 'F5.0', 'F5.6', 'F6.3', 'F7.1', 'F8.0', 'F9.0', 'F10', 'F11', 'F13', 'F14', 'F16',
                 'F18', 'F20', 'F22']

iso_data = ['AUTO', '100', '125', '160', '200', '250', '320', '400', '500', '640', '800', '1000', '1250', '1600',
            '2000', '2500', '3200', '4000', '5000', '6400', '8000', '10000', '12800', '16000', '20000', '25600',
            '32000']

shutter_data = ['30"', '25"', '20"', '15"', '13"', '10"', '8"', '6"', '5"', '4"', '3"2', '2"5', '2"',
                '1"6', '1"3', '1', '0"8', '0"6', '0"5', '0"4', '0"3', '1/4', '1/5', '1/6', '1/8', '1/10',
                '1/13', '1/15', '1/20', '1/25', '1/30', '1/40', '1/50', '1/60', '1/80', '1/100', '1/125',
                '1/160', '1/200', '1/250', '1/320', '1/400', '1/500', '1/640', '1/800', '1/1000',
                '1/1250', '1/1600', '1/2000', '1/2500', '1/3200', '1/4000', '1/5000', '1/6400', '1/8000']


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.control = Control()  # pass in motor step size(cm) for motor1 and 2

        self.m1_direction = 'toEdge'
        self.m2_direction = 'toEdge'

        self.initUI()

    # self.check_box_combo

    def initUI(self):


        self.motor_1_cm = self.set_motor_1_travel()

        self.motor_1_direction = self.motor_1_direction()

        self.manual_move_1 = self.set_manual_move_m1()

        self.manual_move_1.clicked.connect(self.run_move_m1)


        layout = QHBoxLayout()
        #layout.addWidget(self.motor_1_cm)
        #layout.addWidget(self.motor_1_direction)
        layout.addWidget(self.manual_move_1)
        self.setLayout(layout)

        self.motor_1_direction.activated[str].connect(self.m1_dir_onSelected)


    def run_move_m1(self):
        self.control.motor1.moveCm(1.0, "toMotor")




    def m1_dir_onSelected(self, m1_dir):

        self.m1_direction = m1_dir
        print(self.m1_direction)


    def set_motor_1_travel(self):

        mv = QLineEdit()
        mv.setToolTip('This is for the cm the motor travels')
        mv.setFixedWidth(100)
        mv.setFixedHeight(20)

        st = QLabel("Motor 1 Travel \n Length (cm)")
        st.move(50, 500)

        mv.move(50, 530)

        return mv

    def motor_1_direction(self):

        combobox3 = QComboBox(self)
        combobox3.addItem("toEdge")
        combobox3.addItem("toMotor")
        combobox3.setFixedWidth(130)
        combobox3.setFixedHeight(20)
        combobox3.move(180, 530)

        st = QLabel("Motor 1 Direction", self)
        st.move(180, 500)

        return combobox3

    def set_manual_move_m1(self):

        mm1 = QPushButton('Move')
        mm1.setToolTip('to move Motor 1 manually')
        mm1.setFixedWidth(100)
        mm1.setFixedHeight(20)
        mm1.move(340, 530)

        return mm1


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()