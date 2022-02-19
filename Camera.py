import time

from pywinauto import Application
from pywinauto.keyboard import send_keys


class Camera:


    shutter_data = ['30"', '25"', '20"', '15"', '13"', '10"', '8"', '6"', '5"', '4"', '3"2', '2"5', '2"',
                    '1"6', '1"3', '1', '0"8', '0"6', '0"5', '0"4', '0"3', '1/4', '1/5', '1/6', '1/8', '1/10',
                    '1/13', '1/15', '1/20', '1/25', '1/30', '1/40', '1/50', '1/60', '1/80', '1/100', '1/125',
                    '1/160', '1/200', '1/250', '1/320', '1/400', '1/500', '1/640', '1/800', '1/1000',
                    '1/1250', '1/1600', '1/2000', '1/2500', '1/3200', '1/4000', '1/5000', '1/6400', '1/8000']
    aperture_data = ['F4.0', 'F4.5', 'F5.0', 'F5.6', 'F6.3', 'F7.1', 'F8.0', 'F9.0', 'F10', 'F11', 'F13', 'F14',
                     'F16', 'F18', 'F20', 'F22']

    def __init__(self):

        self.start_app()

    def start_app(self):

        try:  # if app1 is already lunched
            self.app = Application().connect(title_re="EOS Utility 3.*")  # title_re="EOS Utility 3.*"
        except:  # if app1 is not launched yet (replace the path)
            self.app = Application().start("C:\Program Files (x86)\Canon\EOS Utility\EU3\EOS Utility 3.exe")
            time.sleep(3)
            self.app = Application().connect(title_re="EOS Utility 3.*")

        time.sleep(3)

        try:  # click 'Remote Shooting' if it shows the top_window
            win = self.app.top_window()
            # win.print_control_identifiers()
            win['Remote Shooting'].click()
            win['Remote Shooting'].click()
        except:  # if it shows the GUI of camera
            pass

        self.app.window(title_re=".*EOS 5D.*")

    def Set_ShutterSpeed(self, shutter_speed_number):

        shutter = self.app.EOS5DMarkIV.child_window(auto_id="olcTv", control_type="EOSUtility.OLCTv").wrapper_object() # Shutter Speed

        shutter.click_input()

        for i in range(shutter_speed_number):
            send_keys('{DOWN}', with_spaces=True)

        send_keys('{ENTER}', with_spaces=True)

    def Set_Aperture(self, Aperture_number):

        aperture = self.app.EOS5DMarkIV.child_window(auto_id="olcAv",control_type="EOSUtility.OLCAv").wrapper_object() # Aperture

        aperture.click_input()

        for i in range(Aperture_number):
            send_keys('{DOWN}', with_spaces=True)

        send_keys('{ENTER}', with_spaces=True)

    def Shoot_Picture(self, shutter_speed_number, aperture_number):

        self.Set_ShutterSpeed(shutter_speed_number)
        self.Set_Aperture(aperture_number)

        shoot = self.app.EOS5DMarkIV.child_window(auto_id="takePictureButton",control_type="EOSUtility.TakePictureButton").wrapper_object()  # This magically works too for picture shooting

        time.sleep(6)
        shoot.click()
        # shoot.move_mouse_input()
        # shoot.press_mouse_input()
        # time.sleep(1)
        # shoot.release_mouse_input()

    def Reset_Count(self, mode): # 55 options for shutter speed, 16 options for aperture

        if mode == "Aperture":

            aperture = self.app.EOS5DMarkIV.child_windowchild_window(auto_id="olcAv",control_type="EOSUtility.OLCAv").wrapper_object()  # Aperture

            aperture.click_input()

            for i in range(16):
                send_keys('{UP}', with_spaces=True)
            send_keys('{ENTER}', with_spaces=True)

        else:

            shutter = self.app.EOS5DMarkIV.child_window(auto_id="olcTv",control_type="EOSUtility.OLCTv").wrapper_object()  # Shutter Speed

            shutter.click_input()

            for i in range(55):
                send_keys('{UP}', with_spaces=True)
            send_keys('{ENTER}', with_spaces=True)

    def get_shutter_number(self, shutter_name):

        s_index = Camera.shutter_data.index(shutter_name)

        return s_index

    def get_aperture_number(self, aperture_name):

        a_index = Camera.aperture_data.index(aperture_name)

        return a_index


Camera1 = Camera()

Camera1.Shoot_Picture(0,4)

# print(Camera1.get_mode_number('1/60','F7.1')[0])

