import unittest
from unittest.mock import patch
import requests

from web.basic_requests import get_current_conditions_by_location_key


class TestGetCurrentConditionsByLocationKey(unittest.TestCase):
    @patch('requests.get')
    def test_successful_response(self, mock_get):
        # Настраиваем мок для успешного ответа API
        mock_response = unittest.mock.Mock()
        mock_response.raise_for_status = unittest.mock.Mock()
        mock_response.json.return_value = {
            'DailyForecasts': [{
                'Temperature': {
                    'Minimum': {'Value': 50.0},
                    'Maximum': {'Value': 77.0}
                },
                'Day': {
                    'Wind': {'Speed': {'Value': 10.0}},  # скорость ветра в милях в час
                    'PrecipitationProbability': 30
                }
            }]
        }
        mock_get.return_value = mock_response

        result = get_current_conditions_by_location_key("12345")
        # Проверяем, что функция возвращает правильные значения (конвертированные)
        self.assertEqual(result, (10.0, 25.0, 16.1, 30))

    @patch('requests.get')
    def test_api_error(self, mock_get):
        # Настраиваем мок для ошибки при запросе (например, неверный API ключ)
        mock_response = unittest.mock.Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Client Error: Unauthorized for url")
        mock_get.return_value = mock_response

        result = get_current_conditions_by_location_key("12345")
        self.assertIsInstance(result, requests.exceptions.HTTPError)

    @patch('requests.get')
    def test_empty_response(self, mock_get):
        # Настраиваем мок для пустого ответа API (пустой словарь)
        mock_response = unittest.mock.Mock()
        mock_response.raise_for_status = unittest.mock.Mock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        result = get_current_conditions_by_location_key("12345")
        self.assertIsInstance(result, KeyError)

    @patch('requests.get')
    def test_unexpected_structure(self, mock_get):
        # Настраиваем мок для ответа с неожиданной структурой данных
        mock_response = unittest.mock.Mock()
        mock_response.raise_for_status = unittest.mock.Mock()
        mock_response.json.return_value = {
            'UnexpectedKey': 'Value'
        }
        mock_get.return_value = mock_response

        result = get_current_conditions_by_location_key("12345")
        self.assertIsInstance(result, KeyError)

    @patch('requests.get')
    def test_network_error(self, mock_get):
        # Настраиваем мок для ошибки сети
        mock_get.side_effect = requests.exceptions.ConnectionError("Network Error")

        result = get_current_conditions_by_location_key("12345")
        self.assertIsInstance(result, requests.exceptions.ConnectionError)

if __name__ == '__main__':
    unittest.main()
