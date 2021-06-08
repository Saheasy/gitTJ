#from numpy import interp
from pymata4 import pymata4
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
            'leftX' : 0,
            'leftY' : 0,
            'rightX' : 0,
            'rightY' : 0,
            'sonar': 0, 
            'distance' : 0,
            'light' : 0, 
            'temp' : 0,
            'rot' : 0, 

        }
        self.pins = {
            'pwmOut' : { 
                'leftEnA': 3,
                'leftEnB': 2,
                'rightEnA': 4,
                'rightEnB': 5, 
                },
            'digitalOut' : {
                'leftIn1': 24, 
                'leftIn2': 25, 
                'leftIn3': 22,
                'leftIn4': 23, 
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
        self.board.pwm_write(ena, int( abs(value) * 2 * 0.75 ) )
        return(ena, in1, in2)

    def drive(self):
        self.motorDriver( 
            self.fL, #drives 
            self.pins['pwmOut']['leftEnA'], 
            self.pins['digitalOut']['leftIn1'],
            self.pins['digitalOut']['leftIn2'])
        self.motorDriver( 
            self.bL,
            self.pins['pwmOut']['leftEnB'], 
            self.pins['digitalOut']['leftIn3'],
            self.pins['digitalOut']['leftIn4'])
        self.motorDriver( 
            self.fR, #drives
            self.pins['pwmOut']['rightEnA'], 
            self.pins['digitalOut']['rightIn1'],
            self.pins['digitalOut']['rightIn2'])
        self.motorDriver( 
            self.bR, 
            self.pins['pwmOut']['rightEnB'], 
            self.pins['digitalOut']['rightIn3'],
            self.pins['digitalOut']['rightIn4'])
        
    def run(self):
        while 1:
            self.bR, self.bL, self.fL, self.fR = 60,-60,-60,60
            self.drive()
            
if __name__ == "__main__":
    TJ = robot()
    art.tprint('== TJ ==', font='dog') #big, 
    art.tprint('        Educational Platform', font = 'small')
    art.tprint(' Teleoperational Testbed', font = 'small')

    TJ.run()