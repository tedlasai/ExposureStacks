

import time
from Sony_camera_u_of_t import SonyCameraUT
import keyboard  # for keyboard input

sony_camera = SonyCameraUT(title="Remote")
sony_camera.connect()

for iteration in range(25):
    for i in range(0, 8):
        sony_camera.capture_image(exposure_time="1/10", iso="100", delay_s=1)

    print(f"Iteration {iteration + 1} complete. Press 'space' to continue.")
    # Wait for the user to press 'space' before continuing to the next loop

    keyboard.wait('space')
    time.sleep(10)
