"""
PiicoDev Accelerometer LIS3DH
Simple example to infer tilt-angle from acceleration data
"""

from PiicoDev_LIS3DH import PiicoDev_LIS3DH
from PiicoDev_Unified import sleep_ms # cross-platform compatible sleep function
from time import sleep

motion = PiicoDev_LIS3DH()

xOffset = None
yOffset = None
def calibrateAccelerometer():
    global xOffset 
    global yOffset
    xOffset, yOffset, _ = motion.angle 

def getAltitude():
    global xOffset
    global yOffset
    # if xOffset is None or yOffset is None:
    #     raise TypeError("Have not calibrated accelerometer")
    failed = True
    value = None
    while failed:
        sleep(0.01)
        try:
            value = motion.angle
            failed = False
        except:
            failed = True
    x, y, z = value
    x -= xOffset
    y -= yOffset
    return round(x,2)
