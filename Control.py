from pywinauto import Application
from pywinauto.keyboard import send_keys

from pyfirmata import Arduino, util
import time
import GS_timing as timing

def main():

    unique_shutter_shot()
    unique_aperture_shot()



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