#from numpy import interp
from pymata4 import pymata4
from inputs import get_gamepad
import art 

class streamingMovingAverage:
    def __init__(self, window_size):
        self.window_size = window_size
        self.values = []
        self.sum = 0

    def process(self, value):
        self.values.append(value)
        self.sum += value
        if len(self.values) > self.window_size:
            self.sum -= self.values.pop(0)
        return float(self.sum) / len(self.values)

class robot:
    def __init__(self):
        self.values = {
            'leftX' : 127,
            'leftY' : 127,
            'rightX' : 127,
            'rightY' : 127,
            'sonar': 0, 
            'distance' : 0,
            'light' : 0, 
            'temp' : 0,
            'rot' : 0, 

        }
        self.pins = {
            'pwmOut' : { 
                'leftEnA': 2,
                'leftEnB': 3,
                'rightEnA': 4,
                'rightEnB': 5, 
                },
            'digitalOut' : {
                'leftIn1': 22, 
                'leftIn2': 23, 
                'leftIn3': 24,
                'leftIn4': 25, 
                'rightIn1': 26, 
                'rightIn2': 27, 
                'rightIn3': 28,
                'rightIn4': 29,
                'relay': 53, 
                },
            'analogOut' : {
                'distance': 0,
                'light' : 1,
                'temp' : 2,
                'rot' : 3
                },
            'sonar': {'trigger': 12, 'echo': 13}
            }
        self.board = pymata4.Pymata4()
        [self.board.set_pin_mode_pwm_output(self.pins['pwmOut'][x]) for x in self.pins['pwmOut'] ]
        [self.board.set_pin_mode_pwm_output(self.pins['digitalOut'][x]) for x in self.pins['digitalOut'] ]
        [self.board.set_pin_mode_pwm_output(self.pins['analogOut'][x]) for x in self.pins['analogOut'] ]
        self.board.set_pin_mode_sonar( self.pins['sonar']['trigger'], self.pins['sonar']['echo'] )

    def motorDriver(self, value, ena, in1, in2):
        if value >= 0:
            self.board.digital_write(in1, 0)
            self.board.digital_write(in2, 1)
        if value < 0:
            self.board.digital_write(in1, 1)
            self.board.digital_write(in2, 0)
        self.board.pwm_write(ena, abs(value) * 2 )
        return(ena, in1, in2)

    def drive(self):
        self.motorDriver( 
            self.fL, 
            self.pins['pwmOut']['leftEnA'], 
            self.pins['digitalOut']['leftIn1'],
            self.pins['digitalOut']['leftIn2'])
        self.motorDriver( 
            self.bL, 
            self.pins['pwmOut']['leftEnB'], 
            self.pins['digitalOut']['leftIn3'],
            self.pins['digitalOut']['leftIn4'])
        self.motorDriver( 
            self.fR, 
            self.pins['pwmOut']['rightEnA'], 
            self.pins['digitalOut']['rightIn1'],
            self.pins['digitalOut']['rightIn2'])
        self.motorDriver( 
            self.fR, 
            self.pins['pwmOut']['rightEnB'], 
            self.pins['digitalOut']['rightIn3'],
            self.pins['digitalOut']['rightIn4'])
        

    def holonomicDrive(self, lX, lY, rX, ):
        self.fL = -lY - lX - rX
        self.fR = lY - lX - rX
        self.bL = -lY + lX - rX
        self.bR = lY + lX - rX
        print( [self.fL, self.fR, self.bL, self.bR], end='\r' )
        self.drive()
    
    def tankDrive(self, lY, rY):
        self.fL = lY
        self.fR = -rY
        self.bL = lY
        self.bR = -rY
        print( f'fL: {self.fL} | fR: {self.fR} | bL: {self.bL} | bR: {self.bR}' + ' ' * 20, end='\r' )
        self.drive()

    def run(self):
        while 1:
            events = get_gamepad() #values 0-255 0 == max UP, 0 == max RIGHT
            for event in events:
                if event.code == "ABS_Y":
                    self.values['leftY'] = event.state - 127
                if event.code == "ABS_RZ":
                    self.values['rightY'] = event.state - 127
                if event.code == "ABS_X":
                    self.values['leftX'] = event.state - 127
                if event.code == "ABS_Z":
                    self.values['rightX'] = event.state - 127
                
            self.tankDrive(
                self.values['leftY'],
                self.values['rightY'] )
               


if __name__ == "__main__":
    TJ = robot()
    art.tprint('TJ', font='dog')
    print('Educational Platform')
    print('Teleoperational Testbed')

    TJ.run()