from magnetometer import calibrateCompass, getAzimuth
from accelerometer import calibrateAccelerometer, getAltitude
from display import displayText, displayAltitudeArrow, displayAzimuthArrow, drawLogo, drawPlanet, displayHoldStill
from gps import getCoordinate
from jpl import getAzimuthAltitudeOfPlanet
from RFID import readRFID
from time import sleep

def beginCalibration():
    displayText("Calibrating accelerometer, position telescope barrel level, then scan any tag")
    readRFID()
    calibrateAccelerometer()
    displayText("Accelerometer calibrated!")
    sleep(2)

    displayText("Keep telescope barrel level as you calibrate compass")
    sleep(3)
    displayText("Calibrating compass, rotate the barrel of the compass slowly, this may take 1-2 full turns")
    calibrateCompass()
    displayText("Compass calibrated!")
    sleep(2)

    displayText("Getting GPS Position")
    sleep(2)
    longitude, latitude, height = getCoordinate()
    displayText([f"Longitude: {longitude}°",f"Latitude: {latitude}°",f"Height: {height}km"])
    sleep(2)
    return longitude, latitude, height

def run():
    for i in range(5):
        drawLogo((64,44),40)
        sleep(1)
    sleep(5)
    longitude, latitude, height = beginCalibration()
    while True:
        displayText(["Scan your planet"])
        planet = readRFID().strip()
        # planet = "Moon"
        displayText([planet + " selected"])
        sleep(3)

        targetAzimuth, targetAltitude = getAzimuthAltitudeOfPlanet(planet, longitude, latitude, height)
        targetAzimuth, targetAltitude = round(float(targetAzimuth),2), round(float(targetAltitude),2)

        displayText(["Aiming for","Az: " + str(targetAzimuth) + "°","Alt: " + str(targetAltitude) + "°"])
        print(targetAzimuth, targetAltitude)
        sleep(5)
        #if the target Altitude is below the horizon, no point
        if targetAltitude < 0:
            displayText("Sorry! The planet is below the horizon, please select another planet")
            sleep(3)
            continue
        
        #Adjust Azimuth
        azimuth = getAzimuth()
        try:
            while True:
                if abs(azimuth - targetAzimuth) < 0.5:
                    displayHoldStill()
                    sleep(2)
                    azimuth = getAzimuth()
                    break  
                azimuth = getAzimuth()
                print(f"target: {targetAzimuth}")
                print(f"azimuth: {azimuth}")
                displayAzimuthArrow(azimuth,targetAzimuth)
                sleep(0.2)
        except KeyboardInterrupt:
            pass

        #Adjust Altitude
        altitude = getAltitude()
        try:
            while True:
                if abs(altitude - targetAltitude) < 0.5:
                    displayHoldStill()
                    sleep(2)
                    altitude = getAltitude()
                    break 
                altitude = getAltitude()
                print(f"altitude: {altitude}")
                displayAltitudeArrow(targetAltitude,altitude)
                sleep(0.2)
            
        except KeyboardInterrupt:
            pass

        for i in range(5):
            drawPlanet((64,44),40,planet)
            sleep(1)
        displayText(["Scan any tag to search for new planet"])
        planet = readRFID().strip()
        displayText([])
        sleep(1)


if __name__ == "__main__":
    sleep(2)
    run()
