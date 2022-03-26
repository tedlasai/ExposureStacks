from pywinauto import Application
from pywinauto.keyboard import send_keys

from pyfirmata import Arduino, util
import time
import GS_timing as timing
import Camera
import Motor


#def main(shutter_code, aperature_code, iso_code):

 #   all_combo(shutter_code, aperture_code, iso_code)

class Control():

    def __init__(self, shutter_settings, aperture_name, iso_name):
        self.shutter_settings = shutter_settings
        self.aperture_name =aperture_name
        self.iso_name = iso_name

        self.camera = Camera.Camera()
        self.motor1 = Motor.Motor(directionPin=6, pulsePin=7, cmToPulses= 32400/47 , invertDirection=False)

        self.aperture_number = self.camera.get_aperture_number(self.aperture_name)
        self.iso_number = self.camera.get_iso_number(self.iso_name)

        self.camera.set_aperture(self.aperture_number)
        self.camera.set_iso(self.iso_number)

    def motorMoveStep(self):
        self.motor1.move(1000, "toEdge")



    def captureStack(self):
        for i in self.shutter_settings:
            print(i)
            shutter_number = self.camera.get_shutter_number(i)
            self.camera.shoot_picture_with_set_aperature(shutter_number, )