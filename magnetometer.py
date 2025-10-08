from PiicoDev_QMC6310 import PiicoDev_QMC6310
from PiicoDev_Unified import sleep_ms
from display import displayText
from time import sleep

compass = PiicoDev_QMC6310(range=200)          # Initialise the sensor with 800uT range. Valid ranges: 200, 800, 1200, 3000 uT
compass.setDeclination(11.91)
def calibrateCompass():
    try:
        compass.calibrate()
    except KeyboardInterrupt:
        pass

def getAzimuth():
    heading = compass.readHeading()   # get the heading from the sensor
    while not compass.dataValid():        # Rejects invalid data
        heading = compass.readHeading()   # get the heading from the sensor
    heading = round(heading,2)      # round to the nearest degree
    print( str(heading) + "°")    # print the data with a degree symbol
    return heading
    # raise TypeError("Error reading compass heading")

if __name__ == "__main__":
    calibrateCompass()
    while True:
        getAzimuth()
        sleep(0.2)
