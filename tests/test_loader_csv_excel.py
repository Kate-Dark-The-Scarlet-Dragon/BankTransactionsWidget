import re
from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.loader_csv_excel import (REQUIRED_COLUMNS, convert_data_to_transactions, convert_record_to_transaction,
                                  load_transactions_from_csv, load_transactions_from_xlsx, validate_dataframe)

# region Тесты для функции - load_transactions_from_csv


def test_load_transactions_from_csv_success(valid_dataframe):
    """Успешная загрузка CSV-файла через 'patch pd.read_csv'."""
    with patch("src.loader_csv_excel.pd.read_csv", return_value=valid_dataframe) as mocked_read:
        result = load_transactions_from_csv("some.csv")

    mocked_read.assert_called_once_with("some.csv", sep=";", dtype=str)

    assert len(result) == 1
    assert result[0]["id"] == 1


def test_load_transactions_from_csv_file_not_found():
    """Ошибка отсутствия файла."""
    with patch("src.loader_csv_excel.pd.read_csv", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError, match="Файл не найден: missing.csv"):
            load_transactions_from_csv("missing.csv")


def test_load_transactions_from_csv_empty_file():
    """Ошибка - пустой CSV-файл."""
    with patch(
        "src.loader_csv_excel.pd.read_csv",
        side_effect=pd.errors.EmptyDataError,
    ):
        with pytest.raises(ValueError, match="CSV-файл пуст"):
            load_transactions_from_csv("empty.csv")


def test_load_transactions_from_csv_parser_error():
    """Ошибка преобразования (парсинга) CSV-файла."""
    with patch(
        "src.loader_csv_excel.pd.read_csv",
        side_effect=pd.errors.ParserError("bad token"),
    ):
        with pytest.raises(ValueError, match="Ошибка парсинга CSV-файла"):
            load_transactions_from_csv("bad.csv")


@pytest.mark.parametrize(
    "exc",
    [RuntimeError("boom"), OSError("disk error"), PermissionError("access denied"), KeyError("missing key")],
    # Идентификаторы для тестов
    ids=["runtime", "os", "permission", "key"],
)
def test_load_transactions_from_csv_generic_exception(exc):
    with patch("src.loader_csv_excel.pd.read_csv", side_effect=exc):
        with pytest.raises(
            Exception,
            # Формат сообщения: «Не удалось прочитать CSV-файл: <текст ошибки>»
            match=rf"^Не удалось прочитать CSV-файл: {re.escape(str(exc))}$",
        ) as excinfo:
            load_transactions_from_csv("weird.csv")

    assert type(excinfo.value) is Exception


# endregion

# region Тесты для функции - load_transactions_from_xlsx


def test_load_transactions_from_xlsx_success(valid_dataframe):
    """Успешная загрузка файла XLSX."""
    with patch("src.loader_csv_excel.pd.read_excel", return_value=valid_dataframe) as mocked_read:
        result = load_transactions_from_xlsx("some.xlsx")

    mocked_read.assert_called_once_with("some.xlsx", dtype=str)

    assert len(result) == 1
    assert result[0]["id"] == 1


def test_load_transactions_from_xlsx_file_not_found():
    """Отсутствует указанный файл."""
    with patch("src.loader_csv_excel.pd.read_excel", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError, match="Файл не найден: missing.xlsx"):
            load_transactions_from_xlsx("missing.xlsx")


def test_load_transactions_from_xlsx_value_error():
    """Ошибка во время чтения XLSX-файла."""
    with patch(
        "src.loader_csv_excel.pd.read_excel",
        side_effect=ValueError("wrong format"),
    ):
        with pytest.raises(ValueError, match="Ошибка чтения XLSX-файла"):
            load_transactions_from_xlsx("broken.xlsx")


@pytest.mark.parametrize(
    "exc",
    [RuntimeError("boom"), OSError("disk error"), PermissionError("access denied"), KeyError("missing key")],
    # Идентификаторы для тестов
    ids=["runtime", "os", "permission", "key"],
)
def test_load_transactions_from_xlsx_generic_exception(exc):
    with patch("src.loader_csv_excel.pd.read_excel", side_effect=exc):
        with pytest.raises(
            Exception,
            # Формат сообщения: «Не удалось прочитать XLSX-файл: <текст ошибки>»
            match=rf"^Не удалось прочитать XLSX-файл: {re.escape(str(exc))}$",
        ) as excinfo:
            load_transactions_from_xlsx("weird.xlsx")

    assert type(excinfo.value) is Exception


# endregion

# region Тесты для функции - convert_data_to_transactions


def test_convert_data_to_transactions_single_row(valid_dataframe):
    """Однострочный DataFrame преобразуется в список из одного словаря."""
    result = convert_data_to_transactions(valid_dataframe)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["id"] == 1
    assert result[0]["operationAmount"]["amount"] == "100.50"


def test_convert_data_to_transactions_multiple_rows():
    """Несколько строк корректно преобразуются."""

    multirow_data_frame = pd.DataFrame(
        [
            {
                "id": "1",
                "state": "EXECUTED",
                "date": "2024-01-15",
                "amount": "10",
                "currency_name": "USD",
                "currency_code": "USD",
                "from": "A",
                "to": "B",
                "description": "d1",
            },
            {
                "id": "2",
                "state": "PENDING",
                "date": "2024-01-16",
                "amount": "20",
                "currency_name": "EUR",
                "currency_code": "EUR",
                "from": "C",
                "to": "D",
                "description": "d2",
            },
        ]
    )

    result = convert_data_to_transactions(multirow_data_frame)

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2
    assert result[0]["state"] == "EXECUTED"
    assert result[1]["state"] == "PENDING"


def test_convert_data_to_transactions_skip_nan_rows():
    """Пустые строки отсутствуют в результате."""
    multirows_dataframe = pd.DataFrame(
        [
            {
                "id": "1",
                "state": "CANCELED",
                "date": "d",
                "amount": "1",
                "currency_name": "RUB",
                "currency_code": "RUB",
                "from": "A",
                "to": "B",
                "description": "x",
            },
            {col: None for col in REQUIRED_COLUMNS},
            {
                "id": "2",
                "state": "EXECUTED",
                "date": "d",
                "amount": "3",
                "currency_name": "Dollar",
                "currency_code": "USD",
                "from": "C",
                "to": "D",
                "description": "x",
            },
            {col: None for col in REQUIRED_COLUMNS},
        ]
    )

    result = convert_data_to_transactions(multirows_dataframe)

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2


def test_convert_data_to_transactions_skip_rows_nan_id():
    """Строки с отсутствующими идентификаторами отсутствуют в результате."""
    incorrect_multirows_dataframe = pd.DataFrame(
        [
            {
                "id": "1",
                "state": "OK",
                "date": "d",
                "amount": "1",
                "currency_name": "RUB",
                "currency_code": "RUB",
                "from": "A",
                "to": "B",
                "description": "x",
            },
            {
                "id": None,
                "state": "EXECUTED",
                "date": "d",
                "amount": "1",
                "currency_name": "RUB",
                "currency_code": "RUB",
                "from": "A",
                "to": "B",
                "description": "x",
            },
            {
                "id": None,
                "state": "CANCELED",
                "date": "d",
                "amount": "3",
                "currency_name": "Dollar",
                "currency_code": "USD",
                "from": "C",
                "to": "D",
                "description": "x",
            },
        ]
    )

    result = convert_data_to_transactions(incorrect_multirows_dataframe)

    assert len(result) == 1
    assert result[0]["id"] == 1


def test_convert_data_to_transactions_empty_raises():
    """Ошибка при попытке преобразовать пустой DataFrame."""
    with pytest.raises(ValueError, match="Данные отсутствуют: не удалось прочитать ни одной записи"):
        convert_data_to_transactions(pd.DataFrame())


@pytest.mark.parametrize("bad_record", ["not a dict", None, ("id", "1"), 42])
def test_convert_data_to_transactions_record_not_dict(bad_record):
    """Проверка, что при конвертации в списке элемент не является словарём."""

    # Генерация DataFrame со всеми полями и идентификатором = '1'
    data_frame = pd.DataFrame([{"id": "1", **{c: "x" for c in REQUIRED_COLUMNS[1:]}}])

    with patch.object(pd.DataFrame, "to_dict", return_value=[bad_record]):
        with pytest.raises(ValueError, match="Ошибка конвертации данных: Каждый элемент должен быть словарём"):
            convert_data_to_transactions(data_frame)


@pytest.mark.parametrize(
    "bad_result",
    [
        42,  # int (число)
        "not a list",  # str (строка)
        ("id", "1"),  # tuple (кортеж)
        {"k": "v"},  # dict (словарь)
        None,  # None (пусто)
    ],
    # Идентификаторы для тестов
    ids=["int", "str", "tuple", "dict", "none"],
)
def test_convert_data_to_transactions_not_list(bad_result):
    """Проверка, что при конвертации вернулся не список."""

    # Генерация DataFrame со всеми полями и идентификатором = '1'
    data_frame = pd.DataFrame([{"id": "1", **{c: "x" for c in REQUIRED_COLUMNS[1:]}}])

    with patch.object(pd.DataFrame, "to_dict", return_value=bad_result):
        with pytest.raises(ValueError, match="Ошибка конвертации данных: ожидался список словарей"):
            convert_data_to_transactions(data_frame)


# endregion

# region Тесты для функции - validate_dataframe


def test_validate_dataframe_success(valid_dataframe):
    """Проверка корректного DataFrame."""
    validate_dataframe(valid_dataframe)


@pytest.mark.parametrize("no_data", [None, pd.DataFrame()])
def test_validate_dataframe_no_data(no_data):
    """Проверка на отсутствие данных."""
    with pytest.raises(ValueError, match="Данные отсутствуют: не удалось прочитать ни одной записи"):
        validate_dataframe(no_data)


@pytest.mark.parametrize(
    "present_columns, expected_missing",
    [
        # Отсутствует колонка идентификатора
        (REQUIRED_COLUMNS[1:], ["id"]),
        # Отсутствует последняя колонка
        (REQUIRED_COLUMNS[:-1], ["description"]),
        # Отсутствует несколько колонок посередине
        (["id", "state", "date", "amount", "from", "to", "description"], ["currency_name", "currency_code"]),
        # Присутствует колонка идентификатора
        (["id"], [c for c in REQUIRED_COLUMNS if c != "id"]),
    ],
    # Идентификаторы для тестов
    ids=["missing-first", "missing-last", "missing-two-middle", "missing-all-but-id"],
)
def test_validate_dataframe_missing_columns(present_columns, expected_missing):
    """Ошибка при недостающих колонках."""
    # Произвольный DataFrame (для прохождения проверки, что он не пустой)
    mock_data_frame = pd.DataFrame([{"id": "1"}])

    with patch.object(pd.DataFrame, "columns", new=pd.Index(present_columns)):
        with pytest.raises(
            ValueError, match=rf"^В файле отсутствуют обязательные колонки: {re.escape(str(expected_missing))}$"
        ):
            validate_dataframe(mock_data_frame)


# endregion

# region Тесты для функции - convert_record_to_transaction


def test_convert_record_to_transaction_full(valid_record, valid_transaction):
    """Проверка корректного преобразования записи."""
    result = convert_record_to_transaction(valid_record)

    assert result == valid_transaction

    # Дополнительно - проверяем, что описание валюты совпадает с её кодом
    assert result["operationAmount"]["currency"]["name"] == "USD"
    assert result["operationAmount"]["currency"]["name"] != "Dollar"


@pytest.mark.parametrize(
    "record, expected_id",
    [
        # Все поля пустые (кроме идентификатора)
        (
            {
                "id": "7",
                "state": None,
                "date": None,
                "operationAmount": {
                    "amount": None,
                    "currency": {"name": None, "code": None},
                },
                "description": None,
                "from": None,
                "to": None,
            },
            7,
        ),
        # Присутствует только поле идентификатора
        ({"id": "1"}, 1),
    ],
    # Идентификаторы для тестов
    ids=["all-nones", "missing-keys"],
)
def test_convert_record_to_transaction_empty_values(record, expected_id):
    """Преобразование записей с заполненными идентификаторами и с пустыми/отсутствующими полями."""
    result = convert_record_to_transaction(record)

    assert result["id"] == expected_id
    assert result["state"] == ""
    assert result["date"] == ""
    assert result["operationAmount"]["amount"] == ""
    assert result["operationAmount"]["currency"]["name"] == ""
    assert result["operationAmount"]["currency"]["code"] == ""
    assert result["description"] == ""
    assert result["from"] == ""
    assert result["to"] == ""


# endregion
