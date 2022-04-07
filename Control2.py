from pywinauto import Application
from pywinauto.keyboard import send_keys

from pyfirmata import Arduino, util
import time
import GS_timing as timing
import Camera
import motor
import torch


#def main(shutter_code, aperature_code, iso_code):

 #   all_combo(shutter_code, aperture_code, iso_code)

class Control():

    def __init__(self):

        self.camera = Camera.Camera()
        self.motor1 = motor.Motor(directionPin=6, pulsePin=7, cmToPulses= 812 , invertDirection=False)
        self.motor2 = motor.Motor(directionPin=3, pulsePin=4, cmToPulses=800, invertDirection=True)

        self.torch1 = torch.Torch(pinNumber=2)



    def updateShutterSettings(self, iso_number):
        self.iso_number = iso_number




    def captureStack(self, shutter_settings, aperature_name, iso_name):
        self.aperture_number = self.camera.get_aperture_number(aperature_name)
        self.iso_number = self.camera.get_iso_number(iso_name)

        self.camera.set_aperture(self.aperture_number)
        self.camera.set_iso(self.iso_number)
        for i in shutter_settings:
            shutter_number = self.camera.get_shutter_number(i)
            self.camera.shoot_picture_with_set_aperature(shutter_number, )