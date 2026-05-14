import os

import pytest
import requests

from src.external_api import convert_currency
from unittest.mock import Mock, patch


# Успешный ответ API
@patch("requests.get")
def test_convert_currency_success(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {"success": True, "result": 87.65}
    mock_get.return_value = mock_response

    with patch("os.getenv", return_value="fake_api_key"):
        result = convert_currency(100.0, "USD", "RUB")

    assert result == 87.65

    mock_get.assert_called_once()

    args, kwargs = mock_get.call_args

    assert kwargs["headers"]["apikey"] == "fake_api_key"
    assert kwargs["params"]["from"] == "USD"
    assert kwargs["params"]["to"] == "RUB"
    assert kwargs["params"]["amount"] == 100.0


# Ошибка HTTP (например, 500)
@patch("requests.get")
def test_convert_currency_http_error(mock_get):
    mock_get.side_effect = Exception("HTTP Error 500")

    with patch("os.getenv", return_value="fake_api_key"):
        with pytest.raises(Exception, match="HTTP Error 500"):
            convert_currency(10.0, "EUR", "RUB")


# В ответе API отсутствует поле "result"
@patch("requests.get")
def test_convert_currency_api_returns_success_false(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {"success": True}
    mock_get.return_value = mock_response

    with patch("os.getenv", return_value="fake_api_key"):
        with pytest.raises(Exception, match="В ответе API отсутствует поле 'result'"):
            convert_currency(50.0, "USD", "RUB")


# Ошибки при обращении к API
@pytest.mark.parametrize(
    "exception_class",
    [
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError,
        requests.exceptions.RequestException,
    ],
)
@patch.dict(os.environ, {"EXCHANGE_API_KEY": "test_api_key"})
@patch("requests.get")
def test_convert_currency_request_exception(mock_get, exception_class):
    mock_get.side_effect = exception_class("Simulated network error")

    with pytest.raises(Exception, match="Ошибка при обращении к API конвертации валют: Simulated network error"):
        convert_currency(amount=100.0, from_currency="USD", to_currency="RUB")


# API вернул success=false
@pytest.mark.parametrize(
    "error_data, expected_message",
    [
        ({"error": {"info": "Invalid API key"}}, "Ошибка API: Invalid API key"),
        ({"error": {"code": 404}}, "Ошибка API: Неизвестная ошибка API"),
        ({"error": {}}, "Ошибка API: Неизвестная ошибка API"),
        ({}, "Ошибка API: Неизвестная ошибка API"),
    ],
)
@patch.dict(os.environ, {"EXCHANGE_API_KEY": "test_key"})
@patch("requests.get")
def test_convert_currency_success_false(mock_get, error_data, expected_message):
    # Настраиваем мок-ответ
    mock_response = Mock()
    mock_response.json.return_value = {"success": False, **error_data}
    mock_response.raise_for_status.return_value = None  # Не выбрасывает HTTPError
    mock_get.return_value = mock_response

    # Проверяем, что выбрасывается именно Exception с правильным сообщением
    with pytest.raises(Exception, match=expected_message):
        convert_currency(amount=100.0, from_currency="USD", to_currency="RUB")


# Отсутствует переменная окружения с API-ключом
@patch("requests.get")
def test_convert_currency_missing_api_key(mock_get):
    with patch("os.getenv", return_value=None):
        with pytest.raises(Exception, match="API key.*не найден"):
            convert_currency(100.0, "USD", "RUB")

    mock_get.assert_not_called()  # Запрос не должен выполняться
