import unittest
from unittest import mock
from math import radians
from AirplaneCatcher import AirplaneCatcher
from flightradar24 import *


class TestAirplanes(unittest.TestCase):
    @mock.patch("AirplaneCatcher.FlightRadar24API")
    def test_get_planes_with_bounds(self, mock_fr):
        mock_api_instance = mock_fr.return_value
        mock_api_instance.get_flights.return_value = [
            mock.Mock(latitude=5, longitude=5, altitude=1000),
            mock.Mock(latitude=2, longitude=2, altitude=500),
            mock.Mock(latitude=8, longitude=8, altitude=0),  # Not in the air
        ]
        mock_api_instance.get_bounds = mock.Mock()
        TEST_ZONE = {"tl_y": 52.24, "tl_x": 20.77, "br_y": 52.04, "br_x": 21.16}
        o = AirplaneCatcher()
        o.dist_from_home = mock.Mock(side_effect=lambda lat, lon: lat + lon)
        planes = o.get_planes(TEST_ZONE)
        self.assertEqual(len(planes), 2)
        self.assertEqual(planes[0].latitude, 2)
        self.assertEqual(planes[0].longitude, 2)
        self.assertEqual(planes[1].latitude, 5)
        self.assertEqual(planes[1].longitude, 5)

    @mock.patch("AirplaneCatcher.FlightRadar24API")
    def test_get_planes_without_bounds(self, mock_fr):
        mock_api_instance = mock_fr.return_value
        mock_api_instance.get_flights.return_value = [
            mock.Mock(latitude=5, longitude=5, altitude=1000),
            mock.Mock(latitude=2, longitude=2, altitude=500),
            mock.Mock(latitude=8, longitude=8, altitude=0),  # Not in the air
        ]
        o = AirplaneCatcher()
        o.dist_from_home = mock.Mock(side_effect=lambda lat, lon: lat + lon)
        planes = o.get_planes()
        self.assertEqual(len(planes), 2)
        self.assertEqual(planes[0].latitude, 2)
        self.assertEqual(planes[0].longitude, 2)
        self.assertEqual(planes[1].latitude, 5)
        self.assertEqual(planes[1].longitude, 5)

    @mock.patch("AirplaneCatcher.config")  # Mock the config module
    def test_dist_from_home(self, mock_config):
        # Set up the mock HOME location in radians (e.g., New York City coordinates)
        mock_config.HOME = (radians(40.7128), radians(-74.0060))

        # Initialize the AirplaneCatcher instance
        catcher = AirplaneCatcher()

        # Test coordinates (e.g., Los Angeles coordinates)
        lat = 34.0522
        lon = -118.2437

        # Expected distance (approximately)
        expected_distance = 3936  # This is an approximate value in kilometers

        # Call the method
        distance = catcher.dist_from_home(lat, lon)

        # Assert that the distance is within a reasonable tolerance
        self.assertAlmostEqual(distance, expected_distance, delta=100)

    def test_return_flight_info_empty_list(self):
        o = AirplaneCatcher()
        result = o.return_flight_info([])
        self.assertIsNone(result)

    def test_return_flight_info_non_empty_list(self):
        o = AirplaneCatcher()
        mock_flight = mock.Mock()
        mock_flight.callsign = "ABC123"
        mock_flight.origin_airport_iata = "JFK"
        mock_flight.destination_airport_iata = "LAX"
        mock_flight.ground_speed = 450
        mock_flight.aircraft_code = "A320"
        mock_flight.altitude = 35000

        flights_list = [mock_flight]
        expected_result = {
            "callsign": "ABC123",
            "from": "JFK",
            "to": "LAX",
            "ground_speed": 450,
            "aircraft": "A320",
            "altitude": 35000,
        }
        result = o.return_flight_info(flights_list)
        self.assertEqual(result, expected_result)

    @mock.patch("AirplaneCatcher.sleep", return_value=None)
    @mock.patch.object(AirplaneCatcher, "get_planes")
    def test_run_no_planes(self, mock_get_planes, mock_sleep):
        o = AirplaneCatcher()
        mock_get_planes.side_effect = [[], [{"callsign": "ABC"}]]

        o.run()

        self.assertEqual(mock_get_planes.call_count, 2)
        mock_sleep.assert_called_with(3)

    @mock.patch("AirplaneCatcher.sleep", return_value=None)
    @mock.patch.object(AirplaneCatcher, "get_planes")
    def test_run_with_debug(self, mock_get_planes, mock_sleep):
        o = AirplaneCatcher()
        mock_get_planes.return_value = [{"Callsign": "ABC123"}]

        o.run(debug=True)

        self.assertEqual(mock_get_planes.call_count, 1)
        mock_get_planes.assert_called_with(
            {"tl_y": 52.24, "tl_x": 20.77, "br_y": 52.04, "br_x": 21.16}
        )
        mock_sleep.assert_called_once()


if __name__ == "__main__":
    unittest.main()
