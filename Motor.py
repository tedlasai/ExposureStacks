from pyfirmata import Arduino, util
import time
import GS_timing as timing

class Motor:

    board = Arduino('COM3')

    def __init__(self, directionPin, pulsePin, invertDirection = False):
        self.directionPin = directionPin
        self.pulsePin = pulsePin
        self.invertDirection = invertDirection

    #direction is boolean because it can only be forward or backward
    #True is 1, False is 0
    def setDirection(self, direction):
        #set direction
        if self.invertDirection: #invert controls
            if direction:
                self.board.digital[self.directionPin].write(0)
            else:
                self.board.digital[self.directionPin].write(1)
        else: #normal controls
            if direction:
                self.board.digital[self.directionPin].write(1)
            else:
                self.board.digital[self.directionPin].write(0)

    #direction is boolean because it can only be high or low
    #High is True, Low is False
    def setPulse(self, high):
        #set direction
        if high:
            self.board.digital[self.pulsePin].write(1)
        else:
            self.board.digital[self.pulsePin].write(0)

    def move(self, pulses, direction = False):
        self.setDirection(direction)

        for i in range(pulses):  # 400 pulses per revolution. range (x) / 400 is the number of revolutions
            self.setPulse(False)
            timing.delayMicroseconds(500)
            self.setPulse(True)
            timing.delayMicroseconds(20)

        timing.delay(1000)

# motor = Motor(directionPin=6, pulsePin=7, invertDirection=False)

# motor.move(8000, True)
# motor.move(8000, False)

