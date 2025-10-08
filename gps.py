import serial
import pynmea2
import time

serialPort = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)

def parseGPS(a):
   a = a.decode('utf-8')  # Decode bytes to string
   if a.find('GGA') > 0:
      msg = pynmea2.parse(a)
      print("Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude %s %s" % 
            (msg.timestamp, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.altitude, msg.altitude_units))
      return msg.lon, msg.lat, msg.altitude
   return None, None, None

def getCoordinate(inside = True):
    a = serialPort.readline()
    if inside:
        return (145.133743, -37.910158, 0.055)
    else:
        long, lat, altitude = parseGPS(a)
        while long == None:
            long, lat, altitude = parseGPS(a)
        return None
        
