import GS_timing as timing
from arduino import board


class Motor:

    def __init__(self,directionPin, pulsePin, cmToPulses,  invertDirection = False):

        self.directionPin = board.get_pin('d:{}:o'.format(directionPin))
        self.pulsePin = board.get_pin('d:{}:o'.format(pulsePin))

        self.invertDirection = invertDirection
        self.cmToPulses = cmToPulses


    #direction is boolean because it can only be forward or backward
    #True is 1, False is 0
    def setDirection(self, directionStr):

        if(directionStr == "toMotor"):
            direction = True
        elif(directionStr == "toEdge"):
            direction = False
        else:
            assert False, "Value must be either toMotor or toEdge"

        #set direction
        if self.invertDirection: #invert controls
            if direction:
                self.directionPin.write(0)
            else:
                self.directionPin.write(1)
        else: #normal controls
            if direction:
                self.directionPin.write(1)
            else:
                self.directionPin.write(0)

    #direction is boolean because it can only be high or low
    #High is True, Low is False
    def setPulse(self, high):
        #set direction
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

    def moveCm(self, centimeters, direction ):
        pulses = int(centimeters * self.cmToPulses)
        self.move(pulses, direction)

        timing.delay(1000)

#motor1 = Motor(directionPin=6, pulsePin=7, cmToPulses= 812 ,invertDirection=False) # 32400/47
#motor2 = Motor(directionPin=3, pulsePin=4, cmToPulses= 124444/19, invertDirection=True) #28000/4.5

# add function for centimeters

# 24000 + 4000 +
# 2000 + 1000 + 1000 + 400 = 32400 for a single trip, 47 cm
# motor1.moveCm(20, True) # True -> to the power source 29.5 mark to 25, 4.5 cm difference for 40
# motor1.moveCm(10, "toEdge")
# motor2.moveCm(10, "toMotor")
#motor.moveCm(0.4, True) # False -> to the edge

#setup another motor
#start figuring out display code for datasets(Abdullah's old code)
#set up ISO
# https://www.eecs.yorku.ca/~abuolaim/ eccv_2018_autofocus/supplemental_materials/supplemental_materials.html#dataBrowser