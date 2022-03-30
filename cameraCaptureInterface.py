#!/usr/bin/python

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QComboBox)
from PyQt5ThreadExample import Worker
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QComboBox)
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtGui import QPixmap
import os
import glob
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import Control2 as control
import motor
import time
import time
import traceback, sys
from PyQt5.QtMultimedia import QCameraImageCapture
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import Control2 as control
from motor import Motor
import time
import numpy as np

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



		self.shutter_list = ['30"']
		self.iso_v = 'AUTO'
		self.aperture_v = 'F4.0'

		self.m1_direction = 'toEdge'
		self.m2_direction = 'toEdge'

		self.m1_cm_value = 0
		self.m2_cm_value = 0

		self.motor1 = Motor(directionPin=6, pulsePin=7, cmToPulses=812, invertDirection=False)  # 32400/47
		self.motor2 = Motor(directionPin=3, pulsePin=4, cmToPulses= 800, invertDirection=True)

		self.available_cameras = QCameraInfo.availableCameras()
		if not self.available_cameras:
			# exit the code
			sys.exit()


		self.save_path = os.path.join(os.path.dirname(__file__), 'Exposures', 'Viewing')
		self.select_camera(0)

		self.captureView = QCameraImageCapture(self.camera)

		self.runningCapture = False # variable to track if we are running a capture

		self.initUI()
		# self.check_box_combo

	def initUI(self):


		self.ap_button = self.set_ap_button()
		self.iso_button = self.set_iso_button()

		self.stop_move = self.stop_motor_move()

		self.click_ap(self.ap_button)
		self.click_iso(self.iso_button)

		self.shutter_button = CheckableComboBox()
		self.shutter_button.setFixedWidth(100)
		self.shutter_button.setFixedHeight(20)

		for i in range(len(shutter_data)):
			self.shutter_button.addItem(shutter_data[i])
			# self.combo.addItem('Item {0}'.format(str(i)))
			self.shutter_button.setItemChecked(i, False)

		start_button = self.set_start_button()
		stop_button = self.set_stop_button(start_button)

		self.motor_1_cm = self.set_motor_1_travel()

		# self.m1_cm_value = float(self.motor_1_cm.text())


		self.motor_1_direction = self.motor_1_direction()

		self.motor_2_cm = self.set_motor_2_travel()


		self.motor_2_direction = self.motor_2_direction()

		self.stack_label = self.stacks()
		self.dataset_name_label = self.dataset_name_create_button()

		self.manual_move_1 = self.set_manual_move_m1()
		self.manual_move_2 = self.set_manual_move_m2()

		self.manual_move_1.clicked.connect(self.run_move_m1)
		self.manual_move_2.clicked.connect(self.run_move_m2)

		self.click_m1_direction(self.motor_1_direction)
		self.click_m2_direction(self.motor_2_direction)

		stop_button.clicked.connect(self.stoph)
		start_button.clicked.connect(self.runp)


		self.horizontal_adjust = self.set_hbox(self.ap_button, self.iso_button, self.shutter_button)

		vbox = QVBoxLayout()
		vbox.addLayout(self.horizontal_adjust)
		vbox.addStretch(1)

		self.setLayout(vbox)

		self.VBL = QVBoxLayout()

		self.FeedLabel = QLabel()
		self.horizontal_adjust.addWidget(self.FeedLabel)

		self.click_photo()

		self.labelImage = QLabel(self)
		self.horizontal_adjust.addWidget(self.labelImage)
		#self.update_picture()
		self.captureView.imageSaved.connect(self.update_picture)

		print("HELLO")
		#

		self.setLayout(self.VBL)

		self.setGeometry(200, 100, 1550, 850)  # 200, 100, 1550, 850
		self.setWindowTitle('Exposure Stacks')

		self.show()

		self.control = None

	def display_image(self, init_img):


		self.pixmap = QPixmap(init_img)
		self.pixmap = self.pixmap.scaled(500, 500, QtCore.Qt.KeepAspectRatio, Qt.FastTransformation)
		self.labelImage.setPixmap(self.pixmap)

		#self.labelImage.move(600, 200)

		self.show()

	def click_photo(self):

		# time stamp
		timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")


		if not self.runningCapture:
			folderStore = 'Viewing'
		else:
			folderStore = self.dataset_name_label.text()
		# capture the image and save it on the save path
		captureId = self.captureView.capture(os.path.join(os.path.dirname(__file__), 'Exposures', folderStore,
										  "%s-%04d-%s.jpg" % (
											  self.current_camera_name,
											  self.save_seq,
											  timestamp
										  )))

		#while(True):
			#print("HELLO")


		# increment the sequence
		self.save_seq += 1


		QApplication.processEvents()

	def select_camera(self, i):

		# getting the selected camera
		self.camera = QCamera(self.available_cameras[i])

		# setting view finder to the camera
		# self.camera.setViewfinder(self.viewfinder)

		# setting capture mode to the camera
		self.camera.setCaptureMode(QCamera.CaptureStillImage)

		# if any error occur show the alert
		self.camera.error.connect(lambda: self.alert(self.camera.errorString()))

		# start the camera
		self.camera.start()

		# creating a QCameraImageCapture object
		self.captureView = QCameraImageCapture(self.camera)

		# showing alert if error occur
		self.captureView.error.connect(lambda error_msg, error,
											  msg: self.alert(msg))

		# when image captured showing message
		self.captureView.imageCaptured.connect(lambda d,
													  i: self.status.showMessage("Image captured : "
																			 + str(self.save_seq)))

		# getting current camera name
		self.current_camera_name = self.available_cameras[i].description()

		# inital save sequence
		self.save_seq = 0

	def run_move_m1(self):

		self.m1_cm_value = int(self.motor_1_cm.text())
		print(self.m1_cm_value)
		print(self.m1_direction)
		self.motor1.moveCm(self.m1_cm_value, self.m1_direction)
		self.click_photo()
		self.captureView.imageSaved.connect(self.update_picture)

	def run_move_m2(self):

		self.m2_cm_value = int(self.motor_2_cm.text())
		print(self.m2_cm_value)
		print(self.m2_direction)
		self.motor2.moveCm(self.m2_cm_value, self.m2_direction)

	def stoph(self):

		sys.exit()

	def move_m1(self):

		self.m1_cm_value = float(self.motor_1_cm.text())

	def click_m1_direction(self, motor_1_direction):

		motor_1_direction.activated[str].connect(self.m1_dir_onSelected)

	def m1_dir_onSelected(self, m1_dir):

		self.m1_direction = m1_dir
		print(self.m1_direction)

	def click_m2_direction(self, motor_2_direction):

		motor_2_direction.activated[str].connect(self.m2_dir_onSelected)

	def m2_dir_onSelected(self, m2_dir):

		self.m2_direction = m2_dir
		print(self.m2_direction)

	def ImageUpdateSlot(self, Image):
		self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

	def CancelFeed(self):

		self.Worker1.stop()

	def set_motor_1_travel(self):

		mv = QLineEdit(self)
		mv.setToolTip('This is for the cm the motor travels')
		mv.setFixedWidth(100)
		mv.setFixedHeight(20)

		self.numStacks = QLabel("Motor 1 Travel \n Length (cm)", self)
		self.numStacks.move(50, 500)

		mv.move(50, 530)

		return mv

	def motor_1_direction(self):

		combobox3 = QComboBox(self)
		combobox3.addItem("toEdge")
		combobox3.addItem("toMotor")
		combobox3.setFixedWidth(130)
		combobox3.setFixedHeight(20)
		combobox3.move(180, 530)

		self.numStacks = QLabel("Motor 1 Direction", self)
		self.numStacks.move(180, 500)

		return combobox3

	def set_motor_2_travel(self):

		mv2 = QLineEdit(self)
		mv2.setToolTip('This is for the cm the motor travels')
		mv2.setFixedWidth(100)
		mv2.setFixedHeight(20)

		self.numStacks = QLabel("Motor 2 Travel \n Length (cm)", self)
		self.numStacks.move(50, 600)

		mv2.move(50, 630)

		return mv2

	def motor_2_direction(self):

		combobox4 = QComboBox(self)
		combobox4.addItem("toEdge")
		combobox4.addItem("toMotor")
		combobox4.setFixedWidth(130)
		combobox4.setFixedHeight(20)
		combobox4.move(180, 630)

		self.numStacks = QLabel("Motor 2 Direction", self)
		self.numStacks.move(180, 600)

		return combobox4

	def runp(self):

		start_time = time.time()

		self.setShutterList()

		print(self.shutter_list, self.aperture_v, self.iso_v)



		self.control = control.Control(self.shutter_list, self.aperture_v, self.iso_v, self.m1_cm_value, self.m2_cm_value, self.m1_direction, self.m2_direction) #pass in motor step size(cm) for motor1 and 2

		#On the view
		#Include options to control motor cm, and direction ||||||||||||||||
		#include number slider to control how many stacks to take |||||||||||||||
		#camera view
		#press a button to move the motors left and right |||||||||||||||||||||
		#recalculate cm constants ||||||||||||||||||||||

		#write out a simple file containing |||||||||||||||||
		#shutter_list, aperature_v, iso_v |||||||||||||||||
		#the time the capture started |||||||||||||||||||
		#motor movement for motor 1 and 2 |||||||||||||
		#Number of steps ||||||||||||||||



		stack_number = int(self.stack_label.text())
		print(stack_number)

		shutter_str = "Shutter List is: " + str(self.shutter_list) + "\n"
		ap_str = "Aperture Value is: " + self.aperture_v + "\n"
		iso_str = "ISO Value is: " + self.iso_v + "\n"
		start_str = "Capture start time at: " + str(start_time) + "\n"
		stack_str = "Number of Stacks: " + str(stack_number) + "\n"
		m1_str = "Motor 1 Direction: " + str(self.m1_direction) + '\n'
		m2_str = "Motor 2 Direction: " + str(self.m2_direction) + '\n'

		print("running")
		L = [shutter_str, ap_str, iso_str, start_str, stack_str, m1_str, m2_str]

		folderStore = os.path.join(os.path.dirname(__file__), 'Exposures', self.dataset_name_label.text())
		# capture the image and save it on the save path
		os.makedirs(folderStore, exist_ok=True)
		captureFileName = os.path.join(folderStore, "runSpecs.txt")

		f = open(captureFileName, "w")
		f.writelines(L)
		f.close()
		self.runningCapture = True

		for i in range(stack_number):
			self.run_move_m1()
			self.run_move_m2()
			self.control.captureStack()
			self.click_photo()
			self.captureView.imageSaved.connect(self.update_picture)

		self.runningCapture = False

		end_time = time.time() - start_time

		f = open(captureFileName, "a")
		f.write("Capture end time is: " + str(end_time) + "\n")
		f.close()


	def update_picture(self, a = "", b= ""):


		print(a,b)
		files = list(filter(os.path.isfile, glob.glob(self.save_path + "\\*")))
		files.sort(key=lambda x: os.path.getmtime(x))


		self.display_image(files[-1])
		self.update()  # where self is the name of the window you want to force to update


	def stacks(self):

		numStacks = QLineEdit(self)
		numStacks.setFixedWidth(100)
		numStacks.setFixedHeight(20)


		
		self.numStacks = QLabel("Number of Stacks", self)
		self.numStacks.move(50, 400)

		numStacks.move(50, 430)

		return numStacks

	def dataset_name_create_button(self):
		datasetName = QLineEdit(self)
		datasetName.setFixedWidth(100)
		datasetName.setFixedHeight(20)
		datasetName.move(50, 330)

		self.dataset_name = QLabel("DataSetName", self)
		self.dataset_name.move(50, 300)
		return datasetName

	def set_manual_move_m1(self):

		mm1 = QPushButton('Move', self)
		mm1.setToolTip('to move Motor 1 manually')
		mm1.setFixedWidth(100)
		mm1.setFixedHeight(20)
		mm1.move(340, 530)

		return mm1

	def set_manual_move_m2(self):

		mm2 = QPushButton('Move', self)
		mm2.setToolTip('to move Motor 2 manually')
		mm2.setFixedWidth(100)
		mm2.setFixedHeight(20)
		mm2.move(340, 630)

		return mm2

	def stop_motor_move(self):

		mm3 = QPushButton('Stop Move', self)
		mm3.setToolTip('to move Motor 2 manually')
		mm3.setFixedWidth(100)
		mm3.setFixedHeight(30)
		mm3.move(340, 580)

		return mm3

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
		combobox2.setFixedWidth(100)
		combobox2.setFixedHeight(20)

		return combobox2

	def set_iso_button(self):

		combobox3 = QComboBox()
		combobox3.addItems(iso_data)
		combobox3.setFixedWidth(100)
		combobox3.setFixedHeight(20)

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




def main():
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
    main()