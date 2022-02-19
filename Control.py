import time

import pandas as pd
from pywinauto import Application
from pywinauto.keyboard import send_keys

def main():


    time.sleep(10)

    # win1 = app1.window(title_re=".*EOS 5D.*")

    shutter_speed_number = 2
    Aperture_number = 2
    mode = "Aperture"

    # ShutterSpeed(shutter_speed_number, app1)
    # Aperture(Aperture_number, app1)
    # Shoot_Picture(app1)
    # Reset_Count(app1, mode)


if __name__ == '__main__':
    main()