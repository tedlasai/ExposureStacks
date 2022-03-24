from pywinauto import Application
from pywinauto.keyboard import send_keys

from pyfirmata import Arduino, util
import time
import GS_timing as timing
import Camera
import Motor
from test_dropdown_2 import final_list

def main():

    # shutter_name = '30"'
    shutter_code = final_list[0]
    aperture_code = final_list[1]
    iso_code = final_list[2]
    # unique_shot(shutter_name, aperture_name)

    all_combo(shutter_code, aperture_code, iso_code)

def unique_shot(shutter_name, aperture_name):
    pass

def all_combo(shutter_settings, aperture_name, iso_name):

    camera1 = Camera.Camera()
    motor1 = Motor.Motor(directionPin=6, pulsePin=7, cmToPulses= 32400/47 , invertDirection=False)
    #aperture_name = 'F8.0'
    aperture_number = camera1.get_aperture_number(aperture_name)
    iso_number = camera1.get_iso_number(iso_name)
    print(aperture_number, iso_number)
    camera1.set_aperture(aperture_number)
    camera1.set_iso(iso_number)

    for j in range(5):

        motor1.move(1000, False)

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