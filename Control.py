from pywinauto import Application
from pywinauto.keyboard import send_keys

from pyfirmata import Arduino, util
import time
import GS_timing as timing
import Camera
#import Motor


def main():

    # shutter_name = '30"'
    shutter_code = 1
    aperture_code = 0
    # unique_shot(shutter_name, aperture_name)

    all_combo(shutter_settings = ['8"', '4"', '2"', '1', '0"5', '1/4', '1/8', '1/15', '1/30', '1/60', '1/125', '1/250', '1/500', '1/1000',
                    '1/2000',  '1/4000', '1/8000'])

def unique_shot(shutter_name, aperture_name):
    pass

def all_combo(shutter_settings, aperture_name = 'F8.0'):

    camera1 = Camera.Camera()
   # motor1 = Motor.Motor(directionPin=6, pulsePin=7, invertDirection=False)
    #aperture_name = 'F8.0'
    aperture_number = camera1.get_aperture_number(aperture_name)

    camera1.set_aperture(aperture_number)

    for j in range(5):

       # motor1.move(1000, False)

        for i in shutter_settings:

            print(i)

            shutter_number = camera1.get_shutter_number(i)
            camera1.shoot_picture_with_set_aperature(shutter_number, )




if __name__ == '__main__':
    main()


    # win1 = app1.window(title_re=".*EOS 5D.*")

    # shutter_speed_number = 2
    # Aperture_number = 2
    # mode = "Aperture"

    # ShutterSpeed(shutter_speed_number, app1)
    # Aperture(Aperture_number, app1)
    # Shoot_Picture(app1)
    # Reset_Count(app1, mode)