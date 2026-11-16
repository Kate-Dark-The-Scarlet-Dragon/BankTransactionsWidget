import json
import pytest

from src import utils
from unittest.mock import mock_open, Mock, patch


#===================================================================
#=== Тесты - Загрузка списка транзакций (операций) из JSON-файла ===
#===================================================================

def test_load_from_correct_file(transaction_list):
    """Обработка файла с корректными данными."""
    with patch("builtins.open", mock_open(read_data=json.dumps(transaction_list))):
        result = utils.load_transactions_from_file("correct.json")
        assert result == transaction_list


def test_load_from_empty_file():
    """Обработка пустого файла."""
    with patch("builtins.open", mock_open(read_data="")):
        result = utils.load_transactions_from_file("empty.json")
        assert result == []


def test_load_from_invalid_file():
    """Обработка файла некорректного формата."""
    with patch("builtins.open", mock_open(read_data="{invalid json}")):
        result = utils.load_transactions_from_file("broken.json")
        assert result == []


def test_load_from_invalid_data_not_list():
    """Обработка файла некорректного формата - данные не в виде списка."""
    with patch("builtins.open", mock_open(read_data=json.dumps({"key": "value"}))):
        result = utils.load_transactions_from_file("object.json")
        assert result == []


def test_load_invalid_data_not_list_of_dicts():
    """Обработка файла некорректного формата - данные не в виде списка словарей."""
    with patch("builtins.open", mock_open(read_data=json.dumps([1, 2, 3]))):
        result = utils.load_transactions_from_file("number_list.json")
        assert result == []


def test_load_file_not_found():
    """Обработка при отсутствии файла."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = utils.load_transactions_from_file("not_exist.json")
        assert result == []


def test_permission_error():
    """Обработка при отсутствии доступа к файлу."""
    with patch("builtins.open", side_effect=PermissionError):
        result = utils.load_transactions_from_file("no_permission.json")
        assert result == []


def test_io_error():
    """Обработка при ошибке чтения файла."""
    with patch("builtins.open", side_effect=OSError("Disk error")):
        result = utils.load_transactions_from_file("io_error.json")
        assert result == []


#==================================================================
#=== Тесты - Удалить пустые элементы из загруженного JSON-файла ===
#==================================================================

@pytest.mark.parametrize(
    "value, expected",
    [
        ([3, None, 1, "", {"a": None}, {}, [], 2], [3, 1, {"a": None}, 2]),
        ([[1, None, ""], [], [None, ""]], [[1], []])
    ])
def test_remove_deleted_elements(value, expected):
    """Проверка на корректное удаление пустых элементов."""
    result = utils.remove_empty_operations(value)

    assert result == expected
    assert result is not value


@pytest.mark.parametrize(
    "value",
    [
        None,
        "",
        {"a": 1, "b": None},
        "some string",
        42,
        True
    ])
def test_remove_none_for_delete(value):
    """Проверка, что отсутствуют элементы для удаления - результат без изменений."""
    assert utils.remove_empty_operations(value) is value


#========================================================
#=== Тесты - Проверка на пустой элемент в данных JSON ===
#========================================================

@pytest.mark.parametrize("value", [None, "", {}, []])
def test_check_empty_values(value):
    """Проверка корректных пустых типов"""
    assert utils.is_empty_value(value) is True


@pytest.mark.parametrize("value", [0, False, [1], {"a": 1}, "text"])
def test_check_border_values_not_empty(value):
    """Проверка на не пустые значения: граничные значения, коллекций, текст."""
    assert utils.is_empty_value(value) is False


#==================================================
#=== Тесты - Получить сумму транзакции в рублях ===
#===================================================

def test_rub_transaction(rub_transaction):
    """Проверка на транзакции в рублях."""
    result = utils.get_transaction_amount_in_rub(rub_transaction)

    assert result == 1500.50
    assert isinstance(result, float)


def test_usd_transaction_calls_converter(usd_transaction):
    """Проверка на транзакции в долларах."""
    # Создаём мок для convert_currency
    mock_convert = Mock(return_value=294721.0)

    with patch("src.utils.convert_currency", mock_convert):
        result = utils.get_transaction_amount_in_rub(usd_transaction)

    mock_convert.assert_called_once_with(9824.07, "USD", "RUB")

    assert result == 294721.0


def test_eur_transaction_calls_converter(eur_transaction):
    """Проверка на транзакции в евро."""
    mock_convert = Mock(return_value=8500.0)

    with patch("src.utils.convert_currency", mock_convert):
        result = utils.get_transaction_amount_in_rub(eur_transaction)

    mock_convert.assert_called_once_with(100.00, "EUR", "RUB")

    assert result == 8500.0


def test_conversion_error(usd_transaction):
    """Ошибка при обращении к API при конвертации валюты."""
    mock_convert = Mock(side_effect=Exception("API error"))

    with patch("src.utils.convert_currency", mock_convert):
        with pytest.raises(Exception, match="API error"):
            utils.get_transaction_amount_in_rub(usd_transaction)


def test_incorrect_currency_error(incorrect_currency_transaction):
    """Ошибка при некорректном коде валюты."""
    with pytest.raises(ValueError, match="Не удалось распознать код валюты: TTT"):
        utils.get_transaction_amount_in_rub(incorrect_currency_transaction)
