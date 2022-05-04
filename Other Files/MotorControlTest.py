from pyfirmata import Arduino, util
import time
board = Arduino('/dev/cu.usbmodem143201')

#pin 6 is the direction

#pin 7 is pulse


board.digital[7].write(1)


#moveMotorForward(pulses)
for i in range(3000):
    board.digital[6].write(0)
    board.digital[7].write(0)
    time.sleep(500/1000000.0)
    board.digital[7].write(1)
    time.sleep(10/1000000.0)


time.sleep(2)

for i in range(3000):
    board.digital[6].write(1)
    board.digital[7].write(0)
    time.sleep(500/1000000.0)
    board.digital[7].write(1)
    time.sleep(10/1000000.0)