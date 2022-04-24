import Camera
import motor
import torch

class Control():

    def __init__(self):

        self.camera = Camera.Camera()
        self.motor1 = motor.Motor(directionPin=6, pulsePin=8, cmToPulses= 812 , invertDirection=False)
        self.motor2 = motor.Motor(directionPin=11, pulsePin=13, cmToPulses= 790, invertDirection=True)

        self.torch1 = torch.Torch(pin=2)
        self.torch_stationary = torch.Torch(pin=4)





    def updateShutterSettings(self, iso_number):
        self.iso_number = iso_number


    def setAperatureAndIso(self, aperature_name, iso_name):
        self.aperture_number = self.camera.get_aperture_number(aperature_name)
        self.iso_number = self.camera.get_iso_number(iso_name)

        self.camera.set_aperture(self.aperture_number)
        self.camera.set_iso(self.iso_number)




    def captureStack(self, shutter_settings):

        for i in shutter_settings:
            shutter_number = self.camera.get_shutter_number(i)
            self.camera.shoot_picture_with_set_aperature(shutter_number, )