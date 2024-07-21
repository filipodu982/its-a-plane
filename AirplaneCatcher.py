from math import acos, sin, cos, radians
from flightradar24 import *
import config


class AirplaneCatcher:
    def __init__(self) -> None:
        self.MY_ZONE = config.MY_ZONE

        self.TEST_ZONE = config.TEST_ZONE

        self._frApi = FlightRadar24API()
        self._bounds = self._frApi.get_bounds(self.MY_ZONE)

    def get_planes(self, bound=None):
        """Function looking for planes within specified bounds and returning list with the closest first"""
        if bound is None:
            bound = self._bounds
        else:
            bound = self._frApi.get_bounds(bound)
        flights = self._frApi.get_flights(bounds=bound)
        flights_in_the_air = [f for f in flights if f.altitude > 0]
        return sorted(
            flights_in_the_air,
            key=lambda f: self.dist_from_home(f.latitude, f.longitude),
        )

    def dist_from_home(self, lat, lon):
        """Calculate great circle distance between the plane and home location"""
        EARTH_RADIUS = 6371
        HOME = config.HOME

        lat = radians(lat)
        lon = radians(lon)
        dist = (
            acos(sin(lat) * sin(HOME[0]) + cos(lat) * cos(HOME[0]) * cos(HOME[1] - lon))
            * EARTH_RADIUS
        )
        return dist


if __name__ == "__main__":
    o = AirplaneCatcher()
    TEST_ZONE = {"tl_y": 52.24, "tl_x": 20.77, "br_y": 52.04, "br_x": 21.16}

    samoloty = o.get_planes(TEST_ZONE)
    print(samoloty)
