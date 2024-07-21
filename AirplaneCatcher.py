from math import acos, sin, cos, radians
from flightradar24 import *
import config


class AirplaneCatcher:
    def __init__(self) -> None:
        MY_ZONE = config.MY_ZONE

        TEST_ZONE = config.TEST_ZONE

        self._frApi = FlightRadar24API()
        self._bounds = self._frApi.get_bounds(MY_ZONE)

    def get_planes(self, bound=None):
        """Function looking for planes within specified bounds and returning list with the closest first"""
        # Checking if the bound was provided during function call or shall we use config files
        if bound is None:
            bound = self._bounds
        else:
            bound = self._frApi.get_bounds(bound)
        flights = self._frApi.get_flights(bounds=bound)
        # Filtering which flights are actually in the air
        flights_in_the_air = [f for f in flights if f.altitude > 0]
        # Sort flights in the air by their closeness to home
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

    def return_flight_info(self, flights_list):
        if not flights_list:
            return None
        else:
            closest_flight = {}
            closest_flight["callsign"] = flights_list[0].callsign
            closest_flight["from"] = flights_list[0].origin_airport_iata
            closest_flight["to"] = flights_list[0].destination_airport_iata
            closest_flight["ground_speed"] = flights_list[0].ground_speed
            closest_flight["aircraft"] = flights_list[0].aircraft_code
            closest_flight["altitude"] = flights_list[0].altitude
            return closest_flight


if __name__ == "__main__":  # pragma: no cover
    o = AirplaneCatcher()
    TEST_ZONE = {"tl_y": 52.24, "tl_x": 20.77, "br_y": 52.04, "br_x": 21.16}

    samoloty = o.get_planes(TEST_ZONE)
    closest_flight_info = o.return_flight_info(samoloty)
    print(closest_flight_info)
