from pywinauto import Application
import time

#C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64 - Inspect tool
class SonyCameraUT:
    def __init__(self, title):
        self.title = title
        self.app = None
        self.main_window = None
        self.button = None

        self.exposure_times_list = [
            '30', '25', '20', '15', '13', '10', '8', '6', '5', '4', '3.2', '2.5', '2', '1.6', '1.3', '1',
            '0.8', '0.6', '0.5', '0.4', '1/3', '1/4', '1/5', '1/6', '1/8', '1/10', '1/13', '1/15', '1/20', '1/25',
            '1/30', '1/40', '1/50', '1/60', '1/80', '1/100', '1/125', '1/160', '1/200', '1/250', '1/320', '1/400',
            '1/500',
            '1/640', '1/800', '1/1000', '1/1250', '1/1600', '1/2000', '1/2500', '1/3200', '1/4000', '1/5000', '1/6400',
            '1/8000'
        ]

        self.isos_list = [
            "102400", "80000", "64000", "51200", "40000", "32000", "25600", "20000",
            "16000", "12800", "10000", "8000", "6400", "5000", "4000", "3200", "2500",
            "2000", "1600", "1250", "1000", "800", "640", "500", "400", "320", "250",
            "200", "160", "125", "100", "80", "64", "50", "AUTO"
        ]


    def connect(self):
        self.app = Application(backend="uia").connect(title=self.title)
        self.main_window = self.app.window(title=self.title)
        self.capture_button = self.main_window.child_window(auto_id="1001", control_type="Button").wrapper_object()


        self.exposure_button = self.main_window.child_window(auto_id="1107", control_type="Image").wrapper_object()
        self.exposure_button.click_input(button='left', double=True) #open menu to get exposure list object
        self.exposure_close_button = self.main_window.child_window(auto_id="9000", control_type="Button").wrapper_object()

        self.exposure_close_button.click()
        self.iso_button = self.main_window.child_window(auto_id="1109", control_type="Image").wrapper_object()
        self.iso_button.click_input(button='left', double=True) #open menu to get exposure list object
        self.iso_close_button = self.main_window.child_window(auto_id="9000", control_type="Button").wrapper_object()
        self.iso_close_button.click()
        time.sleep(2)
    def adjust_text_box(self, auto_id, expected_value):
        text_box = self.main_window.child_window(auto_id=auto_id, control_type="Edit")

        if text_box.exists():
            current_value = text_box.get_value()
            print(f"Current value: {current_value}")

            if current_value != expected_value:
                text_box.set_text(expected_value)
                print("Adjusted the value in the text box")

            time.sleep(10)
            print("Waited for 10 seconds")
        else:
            print("Text box not found on the screen")

    # def click_button(self, auto_id, delay_s=10):
    #     button = self.main_window.child_window(auto_id=auto_id, control_type="Button")
    #
    #     if button.exists():
    #         button.click()
    #         print("Clicked on the button")
    #
    #         sleep_time = delay_s
    #         time.sleep(sleep_time)
    #         print("Waited for 10 seconds")
    #     else:
    #         print("Button not found on the screen")

    def select_exposure(self, exposure_idx):
        self.exposure_button.click_input(button='left', double=True) #open menu to get exposure list object
        self.select_in_list(exposure_idx)


    def select_iso(self, iso_idx):
        self.iso_button.click_input(button='left', double=True)  # open menu to get exposure list object
        self.select_in_list(iso_idx)


    def select_in_list(self, idx):
        list_control = self.main_window.child_window(auto_id="9602", control_type="List").wrapper_object()
        for i in range(10):
            list_control.scroll("up", "page")
        for i in range(idx-5):
            list_control.scroll("down", "line")
        list_control.items()[idx].click_input(button='left', double=True)

    def capture_image(self, exposure_time, iso, delay_s=3):

        assert exposure_time in self.exposure_times_list
        assert iso in self.isos_list
        exposure_time_idx = self.exposure_times_list.index(exposure_time)
        iso_idx = self.isos_list.index(iso)

        self.select_exposure(exposure_time_idx)
        self.select_iso(iso_idx)
        self.capture_button.click()


        print("Clicked on the button")

        sleep_time = delay_s
        time.sleep(sleep_time)
        print(f"Waited for {sleep_time} seconds")
