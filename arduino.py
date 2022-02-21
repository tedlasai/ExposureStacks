from pyfirmata import Arduino, util
import time
import GS_timing as timing

board = Arduino('COM9')

#pin 6 is the direction, pin 7 is pulse

board.digital[7].write(1)

board.digital[6].write(0) # changes direction. 0 for right. 1 for left

#moveMotorForward(pulses)

# for i in range(1600): # 400 pulses per revolution. range (x) / 400 is the number of revolutions
#
#     board.digital[7].write(0)
#     timing.delayMicroseconds(500)
#     board.digital[7].write(1)
#     timing.delayMicroseconds(20)

timing.delay(2000)
board.digital[6].write(0)

for i in range(1600):

    board.digital[7].write(1)
    timing.delayMicroseconds(500)

    board.digital[7].write(0)
    timing.delayMicroseconds(10)