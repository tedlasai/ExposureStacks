from camera import Camera
from lightboxcapture.luminaire_manager import LuminaireManager
#this code assumes camera is set to correct aperature, shutter speed, and iso
from omegaconf import DictConfig, OmegaConf
import time
from motor import Motor

my_motor = Motor(directionPin=11, pulsePin=13, cmToPulses=406, invertDirection=True,
                          rotatingMotor=False)  # 790
conf = OmegaConf.load("lightboxcapture/config.yaml")

lm = LuminaireManager(conf)
lm.init()


camera = Camera()
for k in range(0, 3):
    lm.load_lumenscript()
    time.sleep(1) #1s sleep
    for i in range(0,8):
        camera.just_shoot_picture(3)
        lm.increase_lumen_frame()
        #1s sleep
        time.sleep(2)
    #move motor twice (but not on last one obviously)
    if k!=2:
        my_motor.moveCm(2.0, "toMotor")
#RESET
my_motor.moveCm(4.0, "toEdge")
