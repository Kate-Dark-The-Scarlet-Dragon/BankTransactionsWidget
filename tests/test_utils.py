import json
import pytest
from src.utils import load_transactions_from_file, get_transaction_amount_in_rub
from unittest.mock import mock_open, Mock, patch

# region Тесты для функции - load_transactions_from_file


# Успешное чтение JSON из файла
def test_correct_data(transaction_list):
    with patch("builtins.open", mock_open(read_data=json.dumps(transaction_list))):
        result = load_transactions_from_file("correct.json")
        assert result == transaction_list


# Пустой JSON файл
def test_empty_json_file():
    with patch("builtins.open", mock_open(read_data="")):
        result = load_transactions_from_file("empty.json")
        assert result == []


# Некорректный формат JSON файла
def test_invalid_json_file():
    with patch("builtins.open", mock_open(read_data="{invalid json}")):
        result = load_transactions_from_file("broken.json")
        assert result == []


# Некорректный формат данных - не является списком
def test_data_not_list():
    with patch("builtins.open", mock_open(read_data=json.dumps({"key": "value"}))):
        result = load_transactions_from_file("object.json")
        assert result == []


# Некорректный формат данных - не является списком словарей
def test_data_not_list_of_dicts():
    with patch("builtins.open", mock_open(read_data=json.dumps([1, 2, 3]))):
        result = load_transactions_from_file("number_list.json")
        assert result == []


# Файл не найден
def test_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_transactions_from_file("not_exist.json")
        assert result == []


# Нет доступа к чтению
def test_permission_error():
    with patch("builtins.open", side_effect=PermissionError):
        result = load_transactions_from_file("no_permission.json")
        assert result == []


# Ошибка чтения
def test_io_error():
    with patch("builtins.open", side_effect=OSError("Disk error")):
        result = load_transactions_from_file("io_error.json")
        assert result == []


# endregion

# region Тесты для функции - get_transaction_amount_in_rub


# Транзакция - валюта в рублях
def test_rub_transaction(rub_transaction):
    result = get_transaction_amount_in_rub(rub_transaction)

    assert result == 1500.50
    assert isinstance(result, float)


# Транзакция - валюта в долларах
def test_usd_transaction_calls_converter(usd_transaction):
    # Создаём мок для convert_currency
    mock_convert = Mock(return_value=294721.0)

    with patch("src.utils.convert_currency", mock_convert):
        result = get_transaction_amount_in_rub(usd_transaction)

    mock_convert.assert_called_once_with(9824.07, "USD", "RUB")

    assert result == 294721.0


# Транзакция - валюта в евро
def test_eur_transaction_calls_converter(eur_transaction):
    mock_convert = Mock(return_value=8500.0)

    with patch("src.utils.convert_currency", mock_convert):
        result = get_transaction_amount_in_rub(eur_transaction)

    mock_convert.assert_called_once_with(100.00, "EUR", "RUB")

    assert result == 8500.0


# Ошибка при обращении к API при конвертации валюты
def test_conversion_error(usd_transaction):
    mock_convert = Mock(side_effect=Exception("API error"))

    with patch("src.utils.convert_currency", mock_convert):
        with pytest.raises(Exception, match="API error"):
            get_transaction_amount_in_rub(usd_transaction)


# Ошибка при некорректном коде валюты
def test_incorrect_currency_error(incorrect_currency_transaction):
    with pytest.raises(ValueError, match="Не удалось распознать код валюты: TTT"):
        get_transaction_amount_in_rub(incorrect_currency_transaction)


# endregion
