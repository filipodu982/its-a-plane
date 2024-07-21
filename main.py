from math import acos, sin, cos, radians
from flightradar24 import *
import config
from AirplaneCatcher import AirplaneCatcher

MY_ZONE = config.MY_ZONE

TEST_ZONE = config.TEST_ZONE

EARTH_RADIUS = 6371

HOME = config.HOME


def dist_from_home(lat,lon,home):
    """Calculate great circle distance between the plane and home location"""
    lat = radians(lat)
    lon = radians(lon)
    dist = acos(sin(lat)*sin(home[0])+cos(lat)*cos(home[0])*cos(home[1]-lon))*EARTH_RADIUS
    return dist


fr_api = FlightRadar24API()
bounds = fr_api.get_bounds(MY_ZONE)
print(bounds)

flights = fr_api.get_flights(bounds=bounds)

flights_in_the_air = [f for f in flights if f.altitude > 0]

distances = [dist_from_home(f.latitude, f.longitude, HOME) for f in flights_in_the_air]

print(distances)
print(flights_in_the_air)
callsign = flights_in_the_air[0].callsign
destination = flights_in_the_air[0].destination_airport_iata
departue = flights_in_the_air[0].origin_airport_iata
airplane = flights_in_the_air[0].aircraft_code
speed = flights_in_the_air[0].ground_speed

print(callsign, destination, departue, airplane, speed)


o = AirplaneCatcher()
o.get_planes()
