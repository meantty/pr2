import unittest
from unittest.mock import patch

import requests

from web.basic_requests import get_location_key_by_name


class TestGetLocationKeyByName(unittest.TestCase):
    @patch('requests.get')
    def test_successful_response(self, mock_get):
        # Настраиваем мок для успешного ответа API
        mock_response = unittest.mock.Mock()
        mock_response.raise_for_status = unittest.mock.Mock()
        mock_response.json.return_value = [{'Key': '294021', 'LocalizedName': 'Москва'}]
        mock_get.return_value = mock_response

        # Проверяем, что функция возвращает правильный ключ
        result = get_location_key_by_name("Москва")
        self.assertEqual(result, '294021')

    @patch('requests.get')
    def test_api_error(self, mock_get):
        # Настраиваем мок для ошибки при запросе (например, неверный API ключ)
        mock_response = unittest.mock.Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "401 Client Error: Unauthorized for url")
        mock_get.return_value = mock_response

        # Проверяем, что функция возвращает (None, None) при ошибке API
        result = get_location_key_by_name("Москва")
        self.assertEqual(result, (None, None))

    @patch('requests.get')
    def test_empty_response(self, mock_get):
        # Настраиваем мок для пустого ответа API
        mock_response = unittest.mock.Mock()
        mock_response.raise_for_status = unittest.mock.Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        # Проверяем, что функция возвращает (None, None) при пустом ответе
        result = get_location_key_by_name("Неведомый город")
        self.assertEqual(result, (None, None))

    @patch('requests.get')
    def test_unexpected_structure(self, mock_get):
        # Настраиваем мок для ответа с неожиданной структурой данных
        mock_response = unittest.mock.Mock()
        mock_response.raise_for_status = unittest.mock.Mock()
        mock_response.json.return_value = [{'WrongKey': '12345'}]  # Нет 'Key'
        mock_get.return_value = mock_response

        # Проверяем, что функция возвращает (None, None) при неожиданной структуре данных
        result = get_location_key_by_name("Москва")
        self.assertEqual(result, (None, None))

if __name__ == '__main__':
    unittest.main()
