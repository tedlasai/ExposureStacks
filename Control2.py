from pywinauto import Application
from pywinauto.keyboard import send_keys

from pyfirmata import Arduino, util
import time
import GS_timing as timing
import Camera
import motor


#def main(shutter_code, aperature_code, iso_code):

 #   all_combo(shutter_code, aperture_code, iso_code)

class Control():

    def __init__(self, shutter_settings, aperture_name, iso_name, m1_cm, m2_cm, m1_dir, m2_dir):
        self.shutter_settings = shutter_settings
        self.aperture_name = aperture_name
        self.iso_name = iso_name

        self.motor_1_cm = m1_cm
        self.motor_2_cm = m2_cm

        self.motor_1_direction = m1_dir
        self.motor_2_direction = m2_dir

        self.camera = Camera.Camera()
        self.motor1 = motor.Motor(directionPin=6, pulsePin=7, cmToPulses= 812 , invertDirection=False)
        self.motor2 = motor.Motor(directionPin=3, pulsePin=4, cmToPulses=800, invertDirection=True)

        self.aperture_number = self.camera.get_aperture_number(self.aperture_name)
        self.iso_number = self.camera.get_iso_number(self.iso_name)

        self.camera.set_aperture(self.aperture_number)
        self.camera.set_iso(self.iso_number)

    def motor_1_MoveStep(self):
        self.motor1.moveCm(self.motor_1_cm, self.motor_1_direction)

    def motor_2_MoveStep(self):
        self.motor2.moveCm(self.motor_2_cm, self.motor_2_direction)



    def captureStack(self):
        for i in self.shutter_settings:
            print(i)
            shutter_number = self.camera.get_shutter_number(i)
            self.camera.shoot_picture_with_set_aperature(shutter_number, )