from pyfirmata import Arduino, util
import GS_timing as timing


class Torch:

    board = Arduino('COM3')

    def __init__(self, number_of_toggle):

        self.number_of_toggle = number_of_toggle

    def toggle_button(self):

        self.board.digital[2].write(0)
        timing.delay(500)
        self.board.digital[2].write(1)
        timing.delay(500)


    def high_bright(self):

        self.toggle_button()

        self.number_of_toggle = 4

    def medium_bright(self):

        self.toggle_button()
        self.toggle_button()

        self.number_of_toggle = 3

    def low_bright(self):

        self.toggle_button()
        self.toggle_button()
        self.toggle_button()

        self.number_of_toggle = 2

    def blinding(self):

        self.toggle_button()
        self.toggle_button()
        self.toggle_button()
        self.toggle_button()

        self.number_of_toggle = 1


    def torch_off(self):

        for i in range(0, self.number_of_toggle):
            self.toggle_button()


torch1 = Torch(0)

torch1.blinding()
timing.delayMicroseconds(5000000)
torch1.torch_off()

torch1.medium_bright()
timing.delayMicroseconds(5000000)
torch1.torch_off()
