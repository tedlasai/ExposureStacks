from pywinauto import Application
import time

class SonyCamera:
    def __init__(self, title):
        self.title = title
        self.app = None
        self.main_window = None
        self.button = None

    def connect(self, auto_id="1001"):
        self.app = Application(backend="uia").connect(title=self.title)
        self.main_window = self.app.window(title=self.title)
        self.button = self.main_window.child_window(auto_id=auto_id, control_type="Button").wrapper_object()

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


    def click_button(self, delay_s=3):
        start_time = time.time()  # Start measuring time

        # button = self.main_window.child_window(auto_id=auto_id, control_type="Button").wrapper_object()
        end_time = time.time()  # Stop measuring time
        print(f"Time taken for initial button: {end_time - start_time} seconds")
        # if button.exists():
        #     print(f"Time taken for check button existing: {end_time - start_time} seconds")
        self.button.click()
        # end_time = time.time()  # Stop measuring time
        # print(f"Time taken for click button: {end_time - start_time} seconds")
        print("Clicked on the button")

        sleep_time = delay_s
        time.sleep(sleep_time)
        print(f"Waited for {sleep_time} seconds")

        # else:
        #     print("Button not found on the screen")

        # end_time = time.time()  # Stop measuring time
        # print(f"Time taken for the function: {end_time - start_time} seconds")