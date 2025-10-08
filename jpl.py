import requests
from datetime import datetime, timedelta

def getAzimuthAltitudeOfPlanet(planet: str, longitude: float, latitude: float, height: float):
    print(planet,longitude,latitude,height)
    planets = {
        "Mercury": 199,
        "Venus": 299,
        "Moon": 301,
        "Mars": 499,
        "Jupiter": 599,
        "Saturn": 699,
        "Uranus": 799,
        "Neptune": 899,
        "Pluto": 999,
    }
 
    planetID = planets[planet]
    
    start_time = datetime.now()
    end_time = datetime.now() + timedelta(minutes=1)
 
    fractional_start_time = (start_time.hour * 3600 + start_time.minute * 60 + start_time.second + start_time.microsecond / 1e6) / 86400
    formatted_start_time = start_time.strftime('%Y-%b-%d') + f'{fractional_start_time:.8f}'[1:]
    fractional_end_time = (end_time.hour * 3600 + end_time.minute * 60 + end_time.second + end_time.microsecond / 1e6) / 86400
    formatted_end_time = end_time.strftime('%Y-%b-%d') + f'{fractional_end_time:.8f}'[1:]
 
    # Define the URL and parameters
    url = 'https://ssd.jpl.nasa.gov/api/horizons.api'
    params = {
        'format': 'json',
        'COMMAND': planetID,
        'EPHEM_TYPE': "OBSERVER",
        "CENTER": "coord",
        'COORD_TYPE': 'GEODETIC',
        "SITE_COORD": f"'{longitude},{latitude},{height}'",
        'START_TIME': formatted_start_time,
        'STOP_TIME': formatted_end_time,
        'STEP_SIZE': "10m",
        'QUANTITIES': "4",
        'TIME_ZONE': "+10:00"
    }
 
    response = requests.get(url, params=params)
 
    azimuth, altitude = response.text.split("$$SOE")[1].split("$$EOE")[0].replace("\\n","").split()[-2:]
 
    return azimuth, altitude

if __name__ == "__main__":
    print(getAzimuthAltitudeOfPlanet("Moon",145.035736, -37.918018,0.043))