import time

from pywinauto import Application
from pywinauto.keyboard import send_keys
from fractions import Fraction
import GS_timing as timing


class Camera:

    sleepAperatureAndExposureChange = 2000 #ms

    # shutter is the time taken for each exposure; 30" is 30 seconds, 0"8 is 0.8 seconds, 1/20 is 1/20th of a second
    shutter_data = ['30"', '25"', '20"', '15"', '13"', '10"', '8"', '6"', '5"', '4"', '3"2', '2"5', '2"',
                    '1"6', '1"3', '1', '0"8', '0"6', '0"5', '0"4', '0"3', '1/4', '1/5', '1/6', '1/8', '1/10',
                    '1/13', '1/15', '1/20', '1/25', '1/30', '1/40', '1/50', '1/60', '1/80', '1/100', '1/125',
                    '1/160', '1/200', '1/250', '1/320', '1/400', '1/500', '1/640', '1/800', '1/1000',
                    '1/1250', '1/1600', '1/2000', '1/2500', '1/3200', '1/4000', '1/5000', '1/6400', '1/8000']

    # quite honestly im still lost how aperture works, aside from the camera's 'pupils' definitions - raj
    aperture_data = ['F4.0', 'F4.5', 'F5.0', 'F5.6', 'F6.3', 'F7.1', 'F8.0', 'F9.0', 'F10', 'F11', 'F13', 'F14',
                     'F16', 'F18', 'F20', 'F22']

    iso_data = ['AUTO','100', '125', '160', '200', '250', '320', '400', '500', '640', '800', '1000', '1250',
                '1600', '2000', '2500', '3200', '4000', '5000', '6400', '8000', '10000', '12800', '16000', '20000', '25600', '32000']

    def __init__(self):

        self.start_app()
        self.reset_count("aperture")
        self.reset_count("shutter")
        self.reset_count("iso")


    def start_app(self):

        try:  # if app1 is already lunched
            self.app = Application().connect(title_re="EOS Utility 3.*", found_index=0)  # title_re="EOS Utility 3.*"
            self.app.EOS5DMarkIV.set_focus()
        except:  # if app1 is not launched yet (replace the path)
            self.app = Application().start("C:\Program Files (x86)\Canon\EOS Utility\EU3\EOS Utility 3.exe")
            time.sleep(3)
            self.app = Application().connect(title_re="EOS Utility 3.*", found_index=0) # added found_index because the firmware update made everything worse
            time.sleep(3)


        try:  # click 'Remote Shooting' if it shows the top_window
            win = self.app.top_window()
            # win.print_control_identifiers()
            win['Remote Shooting'].click()
            win['Remote Shooting'].click()
        except:  # if it shows the GUI of camera
            pass

        self.app.window(title_re=".*EOS 5D.*")

    def set_shutter_speed(self, shutter_speed_number):

        shutter = self.app.EOS5DMarkIV.child_window(auto_id="olcTv", control_type="EOSUtility.OLCTv").wrapper_object() # Shutter Speed

        shutter.click_input()


        difference = self.shutter_speed_state - shutter_speed_number
        if (difference < 0):
            for i in range(abs(difference)):
                send_keys('{DOWN}', with_spaces=True)
        elif (difference > 0):
            for i in range(difference):
                send_keys('{UP}', with_spaces=True)
        self.shutter_speed_state = shutter_speed_number

        timing.delay(Camera.sleepAperatureAndExposureChange)
        send_keys('{ENTER}', with_spaces=True)
        timing.delay(Camera.sleepAperatureAndExposureChange)

    def set_aperture(self, aperture_number):


        aperture = self.app.EOS5DMarkIV.child_window(auto_id="olcAv",control_type="EOSUtility.OLCAv").wrapper_object() # Aperture

        aperture.click_input()

        difference = self.aperature_state - aperture_number
        if(difference < 0):
            for i in range(abs(difference)):
                send_keys('{DOWN}', with_spaces=True)
        elif(difference > 0):
            for i in range(difference):
                send_keys('{UP}', with_spaces=True)
        self.aperature_state = aperture_number

        timing.delay(Camera.sleepAperatureAndExposureChange)
        send_keys('{ENTER}', with_spaces=True)
        timing.delay(Camera.sleepAperatureAndExposureChange)

    def set_iso(self, iso_number):

        iso = self.app.EOS5DMarkIV.child_window(auto_id="olcIso",
                                                    control_type="EOSUtility.OLCIso").wrapper_object()  # Shutter Speed
        iso.click_input()

        difference = self.iso_state - iso_number
        if (difference < 0):
            for i in range(abs(difference)):
                send_keys('{DOWN}', with_spaces=True)
        elif (difference > 0):
            for i in range(difference):
                send_keys('{UP}', with_spaces=True)
        self.iso_state = iso_number

        timing.delay(Camera.sleepAperatureAndExposureChange)
        send_keys('{ENTER}', with_spaces=True)
        timing.delay(Camera.sleepAperatureAndExposureChange)

    def shoot_picture(self, shutter_speed_number, aperture_number):

        self.set_shutter_speed(shutter_speed_number)
        self.set_aperture(aperture_number)

        shoot = self.app.EOS5DMarkIV.child_window(auto_id="takePictureButton",control_type="EOSUtility.TakePictureButton").wrapper_object()  # This magically works too for picture shooting

        shoot.click()

        #change sleep time depending on shutter speed time
        sleep_time = self.return_sleep_time(Camera.shutter_data[shutter_speed_number])
        timing.delay((sleep_time + 5)*1000)

    def shoot_picture_with_set_aperature(self, shutter_speed_number):

        self.set_shutter_speed(shutter_speed_number)

        shoot = self.app.EOS5DMarkIV.child_window(auto_id="takePictureButton",control_type="EOSUtility.TakePictureButton").wrapper_object()  # This magically works too for picture shooting

        shoot.click()

        #change sleep time depending on shutter speed time
        sleep_time = self.return_sleep_time(Camera.shutter_data[shutter_speed_number])
        timing.delay((sleep_time + 5)*1000)

    def reset_count(self, mode): # 55 options for shutter speed, 16 options for aperture

        if mode == "aperture":

            aperture = self.app.EOS5DMarkIV.child_window(auto_id="olcAv",control_type="EOSUtility.OLCAv").wrapper_object()  # Aperture

            aperture.click_input()

            for i in range(16):
                send_keys('{UP}', with_spaces=True)

            print("aperture reset done")
            timing.delay(Camera.sleepAperatureAndExposureChange)
            send_keys('{ENTER}', with_spaces=True)
            timing.delay(Camera.sleepAperatureAndExposureChange)
            self.aperature_state = 0

        elif mode == "shutter":

            shutter = self.app.EOS5DMarkIV.child_window(auto_id="olcTv",control_type="EOSUtility.OLCTv").wrapper_object()  # Shutter Speed

            shutter.click_input()

            for i in range(55):
                send_keys('{UP}', with_spaces=True)

            print("shutter reset done")
            timing.delay(Camera.sleepAperatureAndExposureChange)
            send_keys('{ENTER}', with_spaces=True)
            timing.delay(Camera.sleepAperatureAndExposureChange)
            self.shutter_speed_state = 0

        else:
            iso = self.app.EOS5DMarkIV.child_window(auto_id="olcIso",
                                                    control_type="EOSUtility.OLCIso").wrapper_object()  # Shutter Speed
            iso.click_input()

            for i in range(27):
                send_keys('{UP}', with_spaces=True)

            print("iso reset done")
            timing.delay(Camera.sleepAperatureAndExposureChange)
            send_keys('{ENTER}', with_spaces=True)
            timing.delay(Camera.sleepAperatureAndExposureChange)
            self.iso_state = 0

    def get_shutter_number(self, shutter_name):

        s_index = Camera.shutter_data.index(shutter_name)

        return s_index

    def return_sleep_time(self, shutter_speed):

        txt = shutter_speed
        new = txt.split('"')

        if len(new) == 2:
            num1 = float(new[0] + '.' + new[1])
            return num1
            # time.sleep(num1)
        else:
            num2 = float(Fraction(new[0]))
            return num2
            # time.sleep(num2)

    def get_aperture_number(self, aperture_name):

        a_index = Camera.aperture_data.index(aperture_name)

        return a_index

    def get_iso_number(self, iso_name):

        iso_index = Camera.iso_data.index(iso_name)

        return iso_index

