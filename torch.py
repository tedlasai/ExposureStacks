import pyfirmata
import GS_timing as timing
from enum import Enum
from arduino import board

class LightStatus(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    FLASHING = 4
    OFF = 5


class Torch:

    def __init__(self, pin):


        self.light_status = LightStatus.OFF

        self.pin =board.get_pin('d:{}:i'.format(pin))
        #self.pin.write(1)




    def toggle_button(self):
        self.pin.mode = pyfirmata.OUTPUT
        self.pin.write(0)
        timing.delay(500)
        self.pin.write(1)
        timing.delay(500)
        self.pin.mode = pyfirmata.INPUT

        if (self.light_status.value <= 4):
            self.light_status = LightStatus(self.light_status.value + 1)
        else:
            self.light_status = LightStatus(1)

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



# torch1.set_light_status(LightStatus.HIGH)
# timing.delayMicroseconds(5000000)
# print(1)
#
# torch1.set_light_status(LightStatus.MEDIUM)
# timing.delayMicroseconds(5000000)
# print(2)
#
# torch1.set_light_status(LightStatus.LOW)
# timing.delayMicroseconds(5000000)
# print(3)
#
# torch1.set_light_status(LightStatus.OFF)
# timing.delayMicroseconds(5000000)
# print(4)
