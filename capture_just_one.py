# from camera import Camera
# from lightboxcapture.luminaire_manager import LuminaireManager
# #this code assumes camera is set to correct aperature, shutter speed, and iso
# from omegaconf import DictConfig, OmegaConf
# import time
# from motor import Motor
# from Sony_camera import SonyCamera
# start_time = time.time()
# my_motor = Motor(directionPin=11, pulsePin=13, cmToPulses=406, invertDirection=True,
#                           rotatingMotor=False)  # 790
# end_time = time.time()  # Stop measuring time
# print(f"Time taken for initial motor: {end_time - start_time} seconds")
# conf = OmegaConf.load("lightboxcapture/config.yaml")
# end_time = time.time()  # Stop measuring time
# print(f"Time taken for initial conf: {end_time - start_time} seconds")
# lm = LuminaireManager(conf)
# lm.init()
# end_time = time.time()  # Stop measuring time
# print(f"Time taken for initial lm: {end_time - start_time} seconds")
# # my_motor.moveCm(-4.0, "toEdge")
# # camera = Camera()
# sony_camera = SonyCamera(title="Remote")
# sony_camera.connect()
# end_time = time.time()  # Stop measuring time
# print(f"Time taken for initial sony: {end_time - start_time} seconds")
# for k in range(0, 3):
#     lm.load_lumenscript()
#     time.sleep(1) #1s sleep
#     for i in range(0,8):
#         # camera.just_shoot_picture(3)
#         sony_camera.click_button()
#         lm.increase_lumen_frame()
#         #1s sleep
#         time.sleep(2)
#     #move motor twice (but not on last one obviously)
#     if k!=2:
#         time.sleep(4)
#         my_motor.moveCm(2.0, "toMotor")
# #RESET
# my_motor.moveCm(4.0, "toEdge")


from camera import Camera
from lightboxcapture.luminaire_manager import LuminaireManager
# this code assumes camera is set to correct aperature, shutter speed, and iso
from omegaconf import DictConfig, OmegaConf
import time
from motor import Motor
from Sony_camera import SonyCamera
import keyboard  # for keyboard input

start_time = time.time()
my_motor = Motor(directionPin=11, pulsePin=13, cmToPulses=406, invertDirection=True, rotatingMotor=False)
end_time = time.time()
print(f"Time taken for initial motor: {end_time - start_time} seconds")

conf = OmegaConf.load("lightboxcapture/config.yaml")
end_time = time.time()
print(f"Time taken for initial conf: {end_time - start_time} seconds")

lm = LuminaireManager(conf)
lm.init()
end_time = time.time()
print(f"Time taken for initial lm: {end_time - start_time} seconds")

sony_camera = SonyCamera(title="Remote")
sony_camera.connect()
end_time = time.time()
print(f"Time taken for initial sony: {end_time - start_time} seconds")

for iteration in range(25):

    lm.load_lumenscript()
    time.sleep(1)  # 1s sleep


    for i in range(0, 8):
        sony_camera.click_button()
        lm.increase_lumen_frame()

    conf = OmegaConf.load("lightboxcapture/config_sensormap.yaml")
    lm = LuminaireManager(conf)
    lm.init()
    lm.load_lumenscript()

    for i in range(0, 6):
        sony_camera.click_button()
        lm.increase_lumen_frame()


    keyboard.wait('space')
    time.sleep(10)
