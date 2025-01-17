from math import acos, sin, cos, radians
from FlightRadar24.api import FlightRadar24API
import config
from time import sleep


class AirplaneCatcher:
    def __init__(self) -> None:
        MY_ZONE = config.MY_ZONE

        TEST_ZONE = config.TEST_ZONE

        self._frApi = FlightRadar24API()
        self._bounds = self._frApi.get_bounds(MY_ZONE)
        self._flights_over_head = []

    @property
    def flight_over_head(self):
        """Getter for getting 1 flight which is currently over my head - closest to HOME from all flights in boundary"""
        return self.return_flight_info(self._flights_over_head)

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
        """Method which formats information about the closest flight and puts it into dict"""
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

    def run(self, debug=None):
        """Class executable which uses either debug bound or real bound
        and then loops over until any plane is detected within the boundary"""
        any_planes = False
        bound = None
        if debug is not None:
            bound = {"tl_y": 52.24, "tl_x": 20.77, "br_y": 52.04, "br_x": 21.16}  # EPWA
            bound = {
                "tl_y": 50.08758452607344,
                "tl_x": 19.64296274327239,
                "br_y": 50.05570708315496,
                "br_x": 19.777111437633874,
            }  # EPKK WEST
        while not any_planes:
            self._flights_over_head = self.get_planes(bound)
            # print(self._flights_over_head)
            sleep(2)
            if not self._flights_over_head:
                sleep(1)
            else:
                any_planes = True


if __name__ == "__main__":  # pragma: no cover
    o = AirplaneCatcher()
    TEST_ZONE = {"tl_y": 52.24, "tl_x": 20.77, "br_y": 52.04, "br_x": 21.16}

    samoloty = o.get_planes(TEST_ZONE)
    closest_flight_info = o.return_flight_info(samoloty)
    print(closest_flight_info)
