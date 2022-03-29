
from pywinauto import Application
from pywinauto.keyboard import send_keys

from pyfirmata import Arduino, util
import time
import GS_timing as timing
import Camera
import motor


def main():

    # shutter_name = '30"'
    shutter_code = 1
    aperture_code = 0
    # unique_shot(shutter_name, aperture_name)

    #first test is at aperature F80 and Iso_name = 100, numSteps = 90
    #second test is apaerate F20.0 and ISo =100,

    all_combo(shutter_settings = ['20"', '15"', '13"', '10"', '6"', '4"', '2"',
     '1"6', '1', '0"8', '0"5',  '0"3', '1/5', '1/8',  '1/15','1/25', '1/40', '1/60', '1/100',
     '1/160', '1/250', '1/400', '1/640', '1/1000', '1/1600', '1/2500'])

def unique_shot(shutter_name, aperture_name):
    pass


def all_combo(shutter_settings, aperture_name = 'F20', iso_name = '100'):

    camera1 = Camera.Camera()
    motor1 = Motor.Motor(directionPin=6, pulsePin=7, cmToPulses= 32400/47 , invertDirection=False)
    motor2 = Motor.Motor(directionPin=3, pulsePin=4, cmToPulses=124444 / 19, invertDirection=True)  # 28000/4.5
    aperture_number = camera1.get_aperture_number(aperture_name)
    iso_number = camera1.get_iso_number(iso_name)
    print(aperture_number, iso_number)
    camera1.set_aperture(aperture_number)
    camera1.set_iso(iso_number)

    numSteps = 90
    for step in range(numSteps):

        motor1.moveCm(0.4, "toEdge") #max: 40 steps
        motor2.moveCm(0.4, "toEdge")
        print(step)
        for i in shutter_settings:

            print(i)

            shutter_number = camera1.get_shutter_number(i)
            camera1.shoot_picture_with_set_aperature(shutter_number, )

main()



    # win1 = app1.windo
    # if __name__ == '__main__':
    #     main()w(title_re=".*EOS 5D.*")

    # shutter_speed_number = 2
    # Aperture_number = 2
    # mode = "Aperture"

    # ShutterSpeed(shutter_speed_number, app1)
    # Aperture(Aperture_number, app1)
    # Shoot_Picture(app1)
    # Reset_Count(app1, mode)