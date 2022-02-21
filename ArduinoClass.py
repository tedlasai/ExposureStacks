from pyfirmata import Arduino, util
import time
import GS_timing as timing

class MotorArduino:

    board = Arduino('COM9')

    def __init__(self):
        pass

    def move_to_power(self, revolutions):

        num_revolutions = revolutions * 400

        self.board.digital[7].write(1)
        self.board.digital[6].write(1) #moves to power

        for i in range(num_revolutions):  # 400 pulses per revolution. range (x) / 400 is the number of revolutions

            self.board.digital[7].write(0)
            timing.delayMicroseconds(500)
            self.board.digital[7].write(1)
            timing.delayMicroseconds(20)

        timing.delay(2000)

    def move_to_edge(self, revolutions):

        num_revolutions = revolutions * 400

        self.board.digital[6].write(0) #moves to edge

        for i in range(num_revolutions):

            self.board.digital[7].write(0)
            timing.delayMicroseconds(500)

            self.board.digital[7].write(1)
            timing.delayMicroseconds(10)

        timing.delay(2000)

motor = MotorArduino()

motor.move_to_power(4)
motor.move_to_edge(4)

