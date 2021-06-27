#from numpy import interp
from pymata4 import pymata4
from inputs import get_gamepad

class robot:
    def __init__(self):
        self.servoPin = 9
        self.enaPin = 5
        self.in1Pin = 6
        self.in2Pin = 7

        self.board = pymata4.Pymata4()
        self.board.set_pin_mode_servo(self.servoPin)
        self.board.set_pin_mode_pwm_output(self.enaPin)
        self.board.set_pin_mode_digital_output(self.in1Pin)
        self.board.set_pin_mode_digital_output(self.in2Pin)

    def drive(self):
        self.board.servo_write(self.servoPin, self.leftx)
        if self.righty >= 0:
            self.board.digital_write(self.in1Pin, 0)
            self.board.digital_write(self.in2Pin, 1)
        if self.righty < 0:
            self.board.digital_write(self.in1Pin, 1)
            self.board.digital_write(self.in2Pin, 0)
        self.board.pwm_write(self.enaPin, int( abs(self.righty) ) )

    def run(self):
        self.leftx, self.lefty, self.rightx, self.righty = 0,0,0,0
        while 1:
            events = get_gamepad() #values 0-255 0 == max UP, 0 == max RIGHT
            for event in events:
                if event.code == "ABS_Y":
                    self.lefty = event.state - 127
                if event.code == "ABS_RZ":
                    self.righty = event.state - 127
                if event.code == "ABS_X":
                    self.leftx = event.state - 127
                if event.code == "ABS_Z":
                    self.rightx = event.state - 127
            self.drive()

if __name__ == "__main__":
    jerke = robot()
    jerke.run()