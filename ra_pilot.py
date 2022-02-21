import time

from pywinauto import Application
from pywinauto.keyboard import send_keys
from subprocess import check_output

program = '.*EOS 5D.*'
# after the pc connected to the carmera by wifi, the app will launch automatically, so the code tries to connect the app first. if it was not launched, it wil start the app. After that, it will find the top_window and try to click 'Remote Shooting', if it is already showing the GUI, it will try to find the window with title =".*EOS 5D.*". Sometimes it fails to click 'Remote Shooting'....

def main():
    # app1 = Application().connect(path="C:\Program Files (x86)\Canon\EOS Utility\EU3\EOS Utility 3.exe")
    try:  # if app1 is already lunched
        app1 = Application().connect(title_re="EOS Utility 3.*")  #title_re="EOS Utility 3.*"
    except:  # if app1 is not lunched yet (replace the path)
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

    # win1.print_control_identifiers()

    Button = app1.EOS5DMarkIV.child_window(auto_id="takePictureButton",control_type="EOSUtility.TakePictureButton").wrapper_object() # This magically works too

    time.sleep(5)

    Button.click_input()

    time.sleep(2)

    Button.click_input()


    time.sleep(3)
    # Button1 = app1.EOS5DMarkIV.child_window(auto_id="olcTv", control_type="EOSUtility.OLCTv").wrapper_object() # Shutter Speed

    # Button2 = app1.EOS5DMarkIV.child_windowchild_window(auto_id="olcAv", control_type="EOSUtility.OLCAv").wrapper_object() # Aperture

    # shutter = app1.EOS5DMarkIV.child_window(auto_id="olcTv", control_type="EOSUtility.OLCTv").wrapper_object() # Shutter Speed
    #
    # shutter.click_input()
    # shutter.click_input()
    # shutter.EOS5DMarkIV.print_control_identifiers()

    # send_keys('{UP}{ENTER}', with_spaces=True)
    # shutter.click_input()

    Button.click_input()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# the id of the shoot button is "takePictureButton"
    # win1['WindowsForms10.Window.8.app.0.e4c6c4_r15_ad147'].click()  # takepictureButton, this doesn't work for there are two buttons has the same tag.
    # win1[' EOS 5D Mark IVWindowsForms10.Window.8.app.0.e4c6c4_r15_ad131'].click()  # another key of takepictureButton, it also doesn't work.
    # I haven't got time to find how to refer this button by other methods.
    # win1['WindowsForms10.Window.8.app.0.e4c6c4_r15_ad121'].click()  # Expo/AEB, this line will show the sub window of Exposure Compensation.

    # win1['WindowsForms10.Window.8.app.0.e4c6c4_r15_ad121'].print_ctrl_ids()
    # above line prints some information about Expo/AEB, didn't have time to try to access it,
    # might need to find it by name, such as win2 = app1.window(title_re=".*AEB.*") ??

    # following are some other buttons other than those written on the paper, not useful for this project.
    # win1['Shooting menuWindowsForms10.Window.8.app.0.e4c6c4_r15_ad19'].click() #WB SHIFT
    # win1['WindowsForms10.Window.8.app.0.e4c6c4_r15_ad126'].click() #Image saving location
    # win1['WindowsForms10.Window.8.app.0.e4c6c4_r15_ad124'].click() # ETERING MODE
    # win1['WindowsForms10.Window.8.app.0.e4c6c4_r15_ad125'].click()  # Image quality
