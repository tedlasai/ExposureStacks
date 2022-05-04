from pyfirmata import Arduino, util
import GS_timing as timing
import pyfirmata

from enum import Enum

class LightStatus(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    FLASHING = 4
    OFF = 5


class ExposureControlBoard(Arduino):
    def __init__(self, com_port='COM3'):
        super().__init__(com_port)


        #self.directionPin1 = self.get_pin('d:{}:o'.format(6))
        #self.pulsePin1 = self.get_pin('d:{}:o'.format(8))

        #self.invertDirection1 = False
        #self.cmToPulses1 = 800

        self.motor1 = ExposureControlBoard.Motor(self, directionPin=6, pulsePin=8, cmToPulses= 812 , invertDirection=False)

        self.torch = ExposureControlBoard.Torch(self, pin =2)
    class Motor():

        def __init__(self, board, directionPin, pulsePin, cmToPulses, invertDirection=False):

            self.board = board
            self.directionPin = board.get_pin('d:{}:o'.format(directionPin))
            self.pulsePin = board.get_pin('d:{}:o'.format(pulsePin))

            self.invertDirection = invertDirection
            self.cmToPulses = cmToPulses

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

        def move(self, pulses, direction):
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

        def moveCm(self, centimeters, direction):
            pulses = int(centimeters * self.cmToPulses)
            self.move(pulses, direction)

            timing.delay(1000)



    class Torch:

        def __init__(self, board, pin):

            self.light_status = LightStatus.OFF

            self.pin = board.get_pin('d:{}:o'.format(pin))

        def toggle_button(self):
            self.pin.mode = pyfirmata.OUTPUT
            self.pin.write(1)
            timing.delay(500)
            self.pin.write(0)
            timing.delay(500)
            self.pin.mode = pyfirmata.INPUT

        def set_light_status(self, light_status):
            # Type checking
            if not isinstance(light_status, LightStatus):
                raise TypeError('light_status must be an instance of LightStatus Enum')

            if (light_status.value - self.light_status.value >= 0):
                numToggles = light_status.value - self.light_status.value
            else:
                numToggles = 5 + light_status.value - self.light_status.value

            for i in range(numToggles):
                self.toggle_button()
                if (self.light_status.value <= 4):
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


#motor1 = motor.Motor(board, directionPin=6, pulsePin=8, cmToPulses= 812 , invertDirection=False)
#motor2 = motor.Motor(board, directionPin=11, pulsePin=13, cmToPulses=800, invertDirection=True)

ecb = ExposureControlBoard()
ecb.torch.toggle_button()
ecb.motor1.moveCm(1.0, "toEdge")
ecb.motor1.moveCm(1.0, "toMotor")
ecb.torch.toggle_button()
ecb.motor1.moveCm(1.0, "toEdge")
ecb.motor1.moveCm(1.0, "toMotor")
ecb.torch.toggle_button()
ecb.motor1.moveCm(1.0, "toEdge")
ecb.torch.toggle_button()
ecb.motor1.moveCm(1.0, "toMotor")

ecb.torch.toggle_button()
#control.motor2.moveCm(2, "toMotor")

#motor1 = Motor(directionPin=6, pulsePin=8, cmToPulses= 812 ,invertDirection=False) # 32400/47
#motor2 = Motor(directionPin=11, pulsePin=13, cmToPulses= 812 ,invertDirection=True) # 32400/47



# control.torch1.toggle_button()
# time.sleep(2)
# control.torch1.toggle_button()
# time.sleep(2)
# control.torch1.toggle_button()
# time.sleep(2)
#otor1.moveCm(2, "toMotor")
#
#control.motor1.moveCm(2, "toMotor")

#control.motor2.moveCm(2, "toMotor")

#motor2.moveCm(40, "toEdge")