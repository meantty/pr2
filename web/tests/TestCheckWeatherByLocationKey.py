import unittest
from unittest.mock import patch
import requests

from web.basic_requests import check_weather_by_location_key


class TestCheckWeatherByLocationKey(unittest.TestCase):

    @patch('basic_requests.get_current_temperature_by_location_key')
    @patch('basic_requests.get_current_conditions_by_location_key')
    def test_favorable_weather(self, mock_get_conditions, mock_get_temperature):
        mock_get_temperature.return_value = (25.0, 'Sunny')
        mock_get_conditions.return_value = (15.0, 30.0, 10.0, 20)

        result = check_weather_by_location_key("12345")
        self.assertEqual(result['weather_summary'], "Погода благоприятная")
        self.assertIsNone(result['temperature_summary'])
        self.assertIsNone(result['wind_summary'])
        self.assertIsNone(result['precipitation_summary'])

    @patch('basic_requests.get_current_temperature_by_location_key')
    @patch('basic_requests.get_current_conditions_by_location_key')
    def test_unfavorable_temperature(self, mock_get_conditions, mock_get_temperature):
        mock_get_temperature.return_value = (40.0, 'Sunny')
        mock_get_conditions.return_value = (-5.0, 38.0, 10.0, 20)

        result = check_weather_by_location_key("12345")
        self.assertEqual(result['temperature_summary'], "Температура неблагоприятная")
        self.assertEqual(result['weather_summary'], "Погода неблагоприятная")

    @patch('basic_requests.get_current_temperature_by_location_key')
    @patch('basic_requests.get_current_conditions_by_location_key')
    def test_strong_wind(self, mock_get_conditions, mock_get_temperature):
        mock_get_temperature.return_value = (20.0, 'Sunny')
        mock_get_conditions.return_value = (10.0, 25.0, 55.0, 20)

        result = check_weather_by_location_key("12345")
        self.assertEqual(result['wind_summary'], "Сильный ветер")
        self.assertEqual(result['weather_summary'], "Погода неблагоприятная")

    @patch('basic_requests.get_current_temperature_by_location_key')
    @patch('basic_requests.get_current_conditions_by_location_key')
    def test_high_precipitation_probability(self, mock_get_conditions, mock_get_temperature):
        mock_get_temperature.return_value = (20.0, 'Cloudy')
        mock_get_conditions.return_value = (10.0, 25.0, 10.0, 80)

        result = check_weather_by_location_key("12345")
        self.assertEqual(result['precipitation_summary'], "Высокая вероятность осадков")
        self.assertEqual(result['weather_summary'], "Погода неблагоприятная")

    @patch('basic_requests.get_current_temperature_by_location_key')
    @patch('basic_requests.get_current_conditions_by_location_key')
    def test_error_in_temperature_fetch(self, mock_get_conditions, mock_get_temperature):
        mock_get_temperature.side_effect = requests.exceptions.ConnectionError("Network Error")
        mock_get_conditions.return_value = (10.0, 25.0, 10.0, 20)

        with self.assertRaises(ValueError) as context:
            check_weather_by_location_key("12345")
        self.assertIn("Произошла ошибка при обработке погодных данных", str(context.exception))

    @patch('basic_requests.get_current_temperature_by_location_key')
    @patch('basic_requests.get_current_conditions_by_location_key')
    def test_error_in_conditions_fetch(self, mock_get_conditions, mock_get_temperature):
        mock_get_temperature.return_value = (20.0, 'Sunny')
        mock_get_conditions.side_effect = requests.exceptions.HTTPError("API Error")

        with self.assertRaises(ValueError) as context:
            check_weather_by_location_key("12345")
        self.assertIn("Произошла ошибка при обработке погодных данных", str(context.exception))

if __name__ == '__main__':
    unittest.main()
