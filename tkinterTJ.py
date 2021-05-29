from tkinter import *
from tkinter import ttk
import time
from pymata4 import pymata4
import sys
from numpy import interp

global sensorDict

sensorDict = {
    "distanceSensor": {
        "pin":0,
        "type": "analog",
        "io": "input",
        "value": "null",
        "docs": ["https://www.aranacorp.com/en/using-a-distance-sensor-gp2y0a21-arduino/"]},
    "lightSensor": {
        "pin":1,
        "type": "analog",
        "io": "input",
        "value": "null",
        "docs": ["https://wiki.dfrobot.com/DFRobot_Ambient_Light_Sensor_SKU_DFR0026"]},
    "tempSensor": {
        "pin":2,
        "type": "analog",
        "io": "input",
        "value": "null",
        "docs": ["https://wiki.dfrobot.com/DFRobot_LM35_Linear_Temperature_Sensor__SKU_DFR0023_"]},
    "relay": {
        "pin":22,
        "type": "digital",
        "io": "input",
        "value": 0,
        "docs": ["https://wiki.dfrobot.com/Tutorial__DFR0017_V2_Relay", "https://wiki.dfrobot.com/Relay_Module__Arduino_Compatible___SKU__DFR0017_"]},
    "rotSensor": {
        "pin":3,
        "type": "analog",
        "io": "input",
        "value": "null",
        "docs": ["https://wiki.dfrobot.com/Analog_Rotation_Sensor_V2__SKU__DFR0058_"]},
    "ultrasonicSensor": {
        "triggerPin": 12,
        "echoPin":13,
        "type": "digital",
        "value": "null",
        "docs": ["https://wiki.dfrobot.com/DFRobot_LM35_Linear_Temperature_Sensor__SKU_DFR0023_"]}
    }

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

class window:
    
    def __init__(self, root):

        root.title("TJ-Collaborative Robotics Platform")
        root.geometry("500x500")
        mainframe = ttk.Frame(root)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.ultrasonicVar = StringVar()
        self.distanceVar = StringVar()
        self.lightVar = StringVar()
        self.tempVar = StringVar()
        self.rotVar = StringVar()
        self.relayVar = StringVar()

        self.ultrasonicAverage = streamingMovingAverage(50)
        self.distanceAverage = streamingMovingAverage(50)
        self.lightAverage = streamingMovingAverage(50)
        self.tempAverage = streamingMovingAverage(50)
        self.rotAverage = streamingMovingAverage(15)
        self.relayAverage = streamingMovingAverage(50)

        ttk.Label(mainframe, text='Data').grid(column=0, row=0, sticky=(W, E))
        ttk.Label(mainframe, text='Ultrasonic').grid(column=0, row=1, sticky=(W, E))
        ttk.Label(mainframe, textvariable= self.ultrasonicVar).grid(column=1, row=1)
        ttk.Label(mainframe, text='Distance').grid(column=0, row=2, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.distanceVar).grid(column=1, row=2)
        ttk.Label(mainframe, text='Light').grid(column=0, row=3, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.lightVar).grid(column=1, row=3)
        ttk.Label(mainframe, text='Temperature').grid(column=0, row=4, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.tempVar).grid(column=1, row=4)
        ttk.Label(mainframe, text='Rotations').grid(column=0, row=5, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.rotVar).grid(column=1, row=5)
        ttk.Label(mainframe, text='Relay').grid(column=0, row=6, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.relayVar).grid(column=1, row=6)
        
        self.board = pymata4.Pymata4()
        self.board.set_pin_mode_sonar( sensorDict["ultrasonicSensor"]["triggerPin"], sensorDict["ultrasonicSensor"]["triggerPin"], self.ultrasonicCallback)
        self.board.set_pin_mode_analog_input(sensorDict["distanceSensor"]["pin"], callback=self.distanceCallback, differential = 10)
        self.board.set_pin_mode_analog_input(sensorDict["lightSensor"]["pin"], callback=self.lightCallback, differential = 10)
        self.board.set_pin_mode_analog_input(sensorDict["tempSensor"]["pin"], callback=self.tempCallback)
        self.board.set_pin_mode_analog_input(sensorDict["rotSensor"]["pin"], callback=self.rotCallback)


    def distanceCalc(self, value):
        return(((67870.0 / (value - 3.0)) - 40.0))

    def ultrasonicCallback(self, data):
        value = round(self.ultrasonicAverage.process(data[2]))
        self.ultrasonicVar.set(str(value))
        #print(data[2], end = '\r')

    def distanceCallback(self, data):
        value = round(self.distanceAverage.process(data[2]))
        self.distanceVar.set(str(value))

    def lightCallback(self, data):
        value = round(self.lightAverage.process(data[2]))
        self.lightVar.set( str(value))

    def tempCallback(self, data):
        value = round( self.tempAverage.process(data[2]) * (5/10.24) * 1.8 ) + 32
        self.tempVar.set(str(value))

    def rotCallback(self, data):
        value = round(self.rotAverage.process(interp(data[2], [0, 1023], [0, 255])))
        self.rotVar.set( str(value))

    def relayCallback(self, data):
        #value = self.ultrasonicAverage.process(data[2])
        self.relayVar.set("Meow")

        
root = Tk()
w = window(root)
root.mainloop()