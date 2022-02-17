import time

import pandas as pd
from pywinauto import Application
from pywinauto.keyboard import send_keys

class Camera:

    def __init__(self):
        pass

    program = '.*EOS 5D.*'

    def ShutterSpeed(self, shutter_speed_number, app1):

        shutter = app1.EOS5DMarkIV.child_window(auto_id="olcTv", control_type="EOSUtility.OLCTv").wrapper_object() # Shutter Speed

        shutter.click_input()

        for i in range(shutter_speed_number):
            send_keys('{DOWN}', with_spaces=True)

        send_keys('{ENTER}', with_spaces=True)

    def Aperture(self, Aperture_number, app1):

        aperture = app1.EOS5DMarkIV.child_windowchild_window(auto_id="olcAv",control_type="EOSUtility.OLCAv").wrapper_object() # Aperture

        aperture.click_input()

        for i in range(Aperture_number):
            send_keys('{DOWN}', with_spaces=True)

        send_keys('{ENTER}', with_spaces=True)

    def Shoot_Picture(self, app1):

        shoot = app1.EOS5DMarkIV.child_window(auto_id="takePictureButton",control_type="EOSUtility.TakePictureButton").wrapper_object()  # This magically works too for picture shooting

        shoot.click_input()

    def Reset_Count(self, app1, mode): # 55 options for shutter speed, 16 options for aperture

        if mode == "Aperture":

            aperture = app1.EOS5DMarkIV.child_windowchild_window(auto_id="olcAv",control_type="EOSUtility.OLCAv").wrapper_object()  # Aperture

            aperture.click_input()

            for i in range(16):
                send_keys('{UP}', with_spaces=True)
            send_keys('{ENTER}', with_spaces=True)

        else:

            shutter = app1.EOS5DMarkIV.child_window(auto_id="olcTv",control_type="EOSUtility.OLCTv").wrapper_object()  # Shutter Speed

            shutter.click_input()

            for i in range(55):
                send_keys('{UP}', with_spaces=True)
            send_keys('{ENTER}', with_spaces=True)

    def get_shutter_speed_number(self, Name):

        shutter_data = {
            'Shutter Speed': ['30"', '25"', '20"', '15"', '13"', '10"', '8"', '6"', '5"', '4"', '3"2', '2"5', '2"',
                              '1"6', '1"3', '1', '0"8', '0"6', '0"5', '0"4', '0"3', '1/4', '1/5', '1/6', '1/8', '1/10',
                              '1/13', '1/15', '1/20', '1/25', '1/30', '1/40', '1/50', '1/60', '1/80', '1/100', '1/125',
                              '1/160', '1/200', '1/250', '1/320', '1/400', '1/500', '1/640', '1/800', '1/1000',
                              '1/1250', '1/1600', '1/2000', '1/2500', '1/3200', '1/4000', '1/5000', '1/6400', '1/8000']}

        aperture_data = {
            'Aperture': ['F4.0', 'F4.5', 'F5.0', 'F5.6', 'F6.3', 'F7.1', 'F8.0', 'F9.0', 'F10', 'F11', 'F13', 'F14',
                         'F16', 'F18', 'F20', 'F22']}

        s_df = pd.DataFrame(shutter_data)
        a_df = pd.DataFrame(aperture_data)

    def main():

        try:  # if app1 is already lunched
            app1 = Application().connect(title_re="EOS Utility 3.*")  # title_re="EOS Utility 3.*"
        except:  # if app1 is not launched yet (replace the path)
            app1 = Application().start("C:\Program Files (x86)\Canon\EOS Utility\EU3\EOS Utility 3.exe")
            time.sleep(3)
            app1 = Application().connect(title_re="EOS Utility 3.*")

        time.sleep(3)
        try:  # click 'Remote Shooting' if it shows the top_window
            win = app1.top_window()
            # win.print_control_identifiers()
            win['Remote Shooting'].click()
            win['Remote Shooting'].click()
        except:  # if it shows the GUI of camera
            pass

        time.sleep(10)

        win1 = app1.window(title_re=".*EOS 5D.*")

    if __name__ == '__main__':
        main()