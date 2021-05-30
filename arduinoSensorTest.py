# TJ Collaborative Robotics Platform

# Imports
import time
from pymata4 import pymata4
import sys

#Setup Dictionary
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

#Callbacks
def ultrasonicCallback(data):
    #print(data)
    pass

def distanceCallback(data):
    #print(data)
    pass

def distanceCalc(value):
    return(((67870.0 / (value - 3.0)) - 40.0))

def lightCallback(data):
    #print(data[2], end = '\n')
    pass

def tempCallback(data):
    #print(data[2], end = '\r')
    pass

def rotCallback(data):
    #print(data, end='\r')
    pass

def relayCallback(data):
    pass

#Configuration
board = pymata4.Pymata4()
board.set_pin_mode_sonar( sensorDict["ultrasonicSensor"]["triggerPin"], sensorDict["ultrasonicSensor"]["triggerPin"], ultrasonicCallback )
board.set_pin_mode_analog_input(sensorDict["distanceSensor"]["pin"], callback=distanceCallback, differential = 2)
board.set_pin_mode_analog_input(sensorDict["lightSensor"]["pin"], callback=lightCallback)
board.set_pin_mode_analog_input(sensorDict["tempSensor"]["pin"], callback=tempCallback)
board.set_pin_mode_analog_input(sensorDict["rotSensor"]["pin"], callback=rotCallback)
#board.set_pin_mode_digital_output(sensorDict["relaySensor"]["pin"], callback=relayCallback)

#Actual Code
while 1:
    try:
        time.sleep(0.01)
        print('Ultrasonic: {0} | Distance: {1} | Light: {2} | Temp: {3} | Rot: {4} '.format(
            board.sonar_read(sensorDict["ultrasonicSensor"]["triggerPin"])[0],
            distanceCalc( board.analog_read( sensorDict[ "distanceSensor" ][ "pin" ] ) [0]) ,
            board.analog_read( sensorDict[ "lightSensor" ][ "pin" ] ) [0] ,
            board.analog_read( sensorDict[ "tempSensor" ][ "pin" ] )[0] ,
            board.analog_read( sensorDict[ "rotSensor" ][ "pin" ] )[0] ), end='\r')

    except KeyboardInterrupt:
            board.shutdown()
            sys.exit(0)
    
