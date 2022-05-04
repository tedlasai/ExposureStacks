import pyfirmata
#from pyfirmata import Arduino, util
import GS_timing as timing

import motor
import torch
from enum import Enum


class LightStatus(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    FLASHING = 4
    OFF = 5

class ExposureControlBoard(pyfirmata.Arduino):
    def __init__(self, com_port='COM3'):
        super().__init__(com_port)

        self.directionPin = self.get_pin('d:{}:o'.format(6))
        self.pulsePin = self.get_pin('d:{}:o'.format(8))

        self.invertDirection = False
        self.cmToPulses = 800

        self.light_status = LightStatus.OFF

        self.pin = self.get_pin('d:{}:o'.format(2))

        #self.motor1 = self.directionPin1, self.pulsePin1, self.invertDirection1, self.cmToPulses1

        #self.directionPin2 = self.get_pin('d:{}:o'.format(6))
        #self.pulsePin2 = self.get_pin('d:{}:o'.format(8))
        #self.invertDirection2 = False
        #self.cmToPulses2 = 800

        #self.motor1 = self.directionPin2, self.pulsePin2

        #self.pin = self.get_pin('d:{}:i'.format(2))

    def getMotor(self, motorNumber):
        if (motorNumber == 1):
            return self.motor1
        elif (motorNumber == 2):
            return self.motor2
        else:
            assert ("Motor value must be 1 or 2")

    # direction is boolean because it can only be forward or backward
    # True is 1, False is 0
    def setDirection(self, directionStr):

        if (directionStr == "toMotor"):
            direction = True
        elif (directionStr == "toEdge"):
            direction = False
        else:
            assert False, "Value must be either toMotor or toEdge"

        # set direction
        if self.invertDirection:  # invert controls
            if direction:
                self.directionPin.write(0)
            else:
                self.directionPin.write(1)
        else:  # normal controls
            if direction:
                self.directionPin.write(1)
            else:
                self.directionPin.write(0)

    # direction is boolean because it can only be high or low
    # High is True, Low is False
    def setPulse(self, high):
        # set direction
        if high:
            self.pulsePin.write(1)
        else:
            self.pulsePin.write(0)

    def move(self, motorNumber, pulses, direction):

        print("DIRECTION SET")
        self.setDirection(direction)

        print("PUSLING")
        for i in range(pulses):  # 400 pulses per revolution. range (x) / 400 is the number of revolutions
            print("Pulse False Set")
            self.setPulse(False)
            print("Finished Pulse False Set")
            print("Delay Start")
            timing.delayMicroseconds(500)
            print("Delay Finish")
            self.setPulse(True)
            timing.delayMicroseconds(20)

        print("FINISHED PULSING")
        timing.delay(1000)

    def moveCm(self, motorNumber, centimeters, direction):
        pulses = int(centimeters * self.cmToPulses)
        self.move(motorNumber, pulses, direction)

        timing.delay(1000)






    def toggle_button(self):
        self.pin.write(1)
        timing.delay(500)
        self.pin.write(0)
        timing.delay(500)

    def set_light_status(self, light_status):
        # Type checking
        if not isinstance(light_status, LightStatus):
            raise TypeError('light_status must be an instance of LightStatus Enum')

        if(light_status.value - self.light_status.value >= 0):
            numToggles = light_status.value - self.light_status.value
        else:
            numToggles = 5 + light_status.value - self.light_status.value


        for i in range(numToggles):
            self.toggle_button()
            if(self.light_status.value <= 4):
                self.light_status = LightStatus(self.light_status.value + 1)
            else:
                self.light_status = LightStatus(1)


    def t_mode_to_mode(self, mod):

        if mod == "HIGH":

            return LightStatus.HIGH

        elif mod == "MEDIUM":

            return LightStatus.MEDIUM

        elif mod == "LOW":
            return LightStatus.LOW

        elif mod == "FLASHING":
            return LightStatus.FLASHING

        elif mod == "OFF":

            return LightStatus.OFF


# motor1 = motor.Motor(board, directionPin=6, pulsePin=8, cmToPulses= 812 , invertDirection=False)
# motor2 = motor.Motor(board, directionPin=11, pulsePin=13, cmToPulses=800, invertDirection=True)

ecb = ExposureControlBoard()
ecb.toggle_button()
ecb.moveCm(1, 1.0, "toEdge")
ecb.moveCm(1, 1.0, "toMotor")
ecb.moveCm(1, 1.0, "toEdge")
ecb.toggle_button()
ecb.moveCm(1, 1.0, "toMotor")
ecb.moveCm(1, 1.0, "toEdge")
ecb.moveCm(1, 1.0, "toMotor")
# control.motor2.moveCm(2, "toMotor")

# motor1 = Motor(directionPin=6, pulsePin=8, cmToPulses= 812 ,invertDirection=False) # 32400/47
# motor2 = Motor(directionPin=11, pulsePin=13, cmToPulses= 812 ,invertDirection=True) # 32400/47


# control.torch1.toggle_button()
# time.sleep(2)
# control.torch1.toggle_button()
# time.sleep(2)
# control.torch1.toggle_button()
# time.sleep(2)
# otor1.moveCm(2, "toMotor")
#
# control.motor1.moveCm(2, "toMotor")

# control.motor2.moveCm(2, "toMotor")

# motor2.moveCm(40, "toEdge")