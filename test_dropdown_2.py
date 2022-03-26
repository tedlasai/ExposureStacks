#!/usr/bin/python

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QComboBox)

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import Control2 as control


aperture_data = ['F4.0', 'F4.5', 'F5.0', 'F5.6', 'F6.3', 'F7.1', 'F8.0', 'F9.0', 'F10', 'F11', 'F13', 'F14','F16', 'F18', 'F20', 'F22']

iso_data = ['AUTO', '100', '125', '160', '200', '250', '320', '400', '500', '640', '800', '1000', '1250','1600', '2000', '2500', '3200', '4000', '5000', '6400', '8000', '10000', '12800', '16000', '20000','25600', '32000']

shutter_data = ['30"', '25"', '20"', '15"', '13"', '10"', '8"', '6"', '5"', '4"', '3"2', '2"5', '2"',
                    '1"6', '1"3', '1', '0"8', '0"6', '0"5', '0"4', '0"3', '1/4', '1/5', '1/6', '1/8', '1/10',
                    '1/13', '1/15', '1/20', '1/25', '1/30', '1/40', '1/50', '1/60', '1/80', '1/100', '1/125',
                    '1/160', '1/200', '1/250', '1/320', '1/400', '1/500', '1/640', '1/800', '1/1000',
                    '1/1250', '1/1600', '1/2000', '1/2500', '1/3200', '1/4000', '1/5000', '1/6400', '1/8000']



class Example(QWidget):

	def __init__(self):
		super().__init__()

		self.initUI()

		self.shutter_list = ['30"']
		self.iso_v = 'AUTO'
		self.aperture_v = 'F4.0'

		# self.check_box_combo

	def initUI(self):

		self.ap_button = self.set_ap_button()
		self.iso_button = self.set_iso_button()

		self.click_ap(self.ap_button)
		self.click_iso(self.iso_button)

		self.shutter_button = CheckableComboBox()
		self.shutter_button.setFixedWidth(150)
		self.shutter_button.setFixedHeight(50)
		for i in range(len(shutter_data)):
			self.shutter_button.addItem(shutter_data[i])
			# self.combo.addItem('Item {0}'.format(str(i)))
			self.shutter_button.setItemChecked(i, False)

		start_button = self.set_start_button()
		stop_button = self.set_stop_button(start_button)



		start_button.clicked.connect(self.runp)

		horizontal_adjust = self.set_hbox(self.ap_button, self.iso_button, self.shutter_button)

		vbox = QVBoxLayout()
		vbox.addLayout(horizontal_adjust)
		vbox.addStretch(1)

		self.setLayout(vbox)

		self.VBL = QVBoxLayout()

		self.FeedLabel = QLabel()
		horizontal_adjust.addWidget(self.FeedLabel)

		self.Worker1 = Worker1()
		self.Worker1.start()
		self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
		self.setLayout(self.VBL)

		self.setGeometry(200, 100, 1550, 850)  # 200, 100, 1550, 850
		self.setWindowTitle('Exposure Stacks')
		self.show()

		self.control = None

	def ImageUpdateSlot(self, Image):

		self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

	def CancelFeed(self):

		self.Worker1.stop()

	def runp(self):

		self.setShutterList()

		print(self.shutter_list, self.aperture_v, self.iso_v)

		self.control = control.Control(self.shutter_list, self.aperture_v, self.iso_v) #pass in motor step size(cm) for motor1 and 2


		#On the view
		#Include options to control motor cm, and direction
		#include number slider to control how many stacks to take
		#camera view
		#press a button to move the motors left and right
		#recalculate cm constants

		#write out a simple file containing
		#shutter_list, aperature_v, iso_v
		#the time the capture started
		#motor movement for motor 1 and 2
		#Number of steps


		for i in range(50):
			self.control.motorMoveStep()
			#self.camera.takePicture update THe view
			self.control.captureStack()





	def clean(self):

		# print("is it running?")
		self.shutter_list = []
		# print(shutter_list)

	def click_ap(self, ap_button):

		ap_button.activated[str].connect(self.ap_onSelected)

	def click_iso(self, iso_button):

		iso_button.activated[str].connect(self.iso_onSelected)

	def clear_list(self):

		combobox4 = QPushButton('Clear List')
		combobox4.setFixedWidth(150)
		combobox4.setFixedHeight(50)

		return combobox4

	def ap_onSelected(self, ap):

		self.aperture_v = ap

	def iso_onSelected(self, iso):

		self.iso_v = iso

	def set_ap_button(self):

		combobox2 = QComboBox()
		combobox2.addItems(aperture_data)
		combobox2.setFixedWidth(150)
		combobox2.setFixedHeight(50)

		return combobox2

	def set_iso_button(self):

		combobox3 = QComboBox()
		combobox3.addItems(iso_data)
		combobox3.setFixedWidth(150)
		combobox3.setFixedHeight(50)

		return combobox3

	def set_hbox(self, ap_button, iso_button, shutter_button):

		hbox = QHBoxLayout()
		hbox.addStretch(1)
		hbox.addWidget(ap_button)
		hbox.addWidget(iso_button)
		hbox.addWidget(shutter_button)
		return hbox

	def set_start_button(self):

		btn = QPushButton('Start', self)
		btn.setToolTip('This is a <b>QPushButton</b> widget')
		btn.resize(btn.sizeHint())
		btn.move(50, 120)

		return btn

	def set_stop_button(self, btn):

		btn2 = QPushButton('Stop', self)
		btn2.setToolTip('This is a <b>QPushButton</b> widget')
		btn2.resize(btn.sizeHint())
		btn2.move(50, 180)

		return btn2

	def set_enter_button(self):

		btn3 = QPushButton('Set Settings')
		# btn3.clicked.connect(self.getValue)
		btn3.setFixedWidth(150)
		btn3.setFixedHeight(50)

		return btn3

	def setShutterList(self):

		self.shutter_list = []
		for i in range(self.shutter_button.count()):

			if self.shutter_button.itemChecked(i):
				self.shutter_list.append(shutter_data[i])

		print(self.shutter_list)

class CheckableComboBox(QComboBox):

    def __init__(self):
        super().__init__()
        self._changed = False

        self.view().pressed.connect(self.handleItemPressed)

    def setItemChecked(self, index, checked=False):
        item = self.model().item(index, self.modelColumn())  # QStandardItem object

        if checked:
            item.setCheckState(Qt.Checked)
        else:
            item.setCheckState(Qt.Unchecked)

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)

        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)
        self._changed = True

    def hidePopup(self):
        if not self._changed:
            super().hidePopup()
        self._changed = False

    def itemChecked(self, index):
        item = self.model().item(index, self.modelColumn())
        return item.checkState() == Qt.Checked

class Worker1(QThread):

    ImageUpdate = pyqtSignal(QImage)

    def run(self):

        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(840, 880, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)

    def stop(self):

        self.ThreadActive = False
        self.quit()


def main():
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
    main()