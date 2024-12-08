import unittest
from unittest.mock import patch
import requests

from web.basic_requests import get_location_key_by_coordinates


class TestGetLocationKeyByCoordinates(unittest.TestCase):
    @patch('requests.get')
    def test_successful_response(self, mock_get):
        # Настраиваем мок для успешного ответа API
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {'Key': '67890', 'LocalizedName': 'Москва'}
        mock_get.return_value = mock_response

        # Проверяем, что функция возвращает правильный ключ
        result = get_location_key_by_coordinates(55.7558, 37.6176)
        self.assertEqual(result, '67890')

    @patch('requests.get')
    def test_api_error(self, mock_get):
        # Настраиваем мок для ошибки HTTP
        mock_response = unittest.mock.Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "401 Client Error: Unauthorized for url")
        mock_get.return_value = mock_response

        # Проверяем, что функция возвращает None при ошибке API
        result = get_location_key_by_coordinates(55.7558, 37.6176)
        self.assertIsNone(result)

    @patch('requests.get')
    def test_empty_response(self, mock_get):
        # Настраиваем мок для пустого ответа API
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        # Проверяем, что функция возвращает None при пустом ответе
        result = get_location_key_by_coordinates(55.7558, 37.6176)
        self.assertIsNone(result)

    @patch('requests.get')
    def test_unexpected_structure(self, mock_get):
        # Настраиваем мок для ответа с неожиданной структурой данных
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {'WrongKey': '12345'}  # Нет 'Key'
        mock_get.return_value = mock_response

        # Проверяем, что функция возвращает None при неожиданной структуре данных
        result = get_location_key_by_coordinates(55.7558, 37.6176)
        self.assertIsNone(result)

    @patch('requests.get')
    def test_network_error(self, mock_get):
        # Настраиваем мок для ошибки сети, например, временная недоступность сервиса
        mock_get.side_effect = requests.exceptions.ConnectionError("Network Error")

        # Проверяем, что функция возвращает None при сетевой ошибке
        result = get_location_key_by_coordinates(55.7558, 37.6176)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
