from typing import Any, Hashable

import pandas as pd

# Ожидаемые колонки в исходных файлах
REQUIRED_COLUMNS = ["id", "state", "date", "amount", "currency_name", "currency_code", "from", "to", "description"]


def load_transactions_from_csv(file_path: str) -> list[dict[str, Any]]:
    """
    Загрузка транзакций из CSV-файла.
    :param file_path: Путь к CSV-файлу.
    :return: Список транзакций.
    :raises FileNotFoundError: CSV-файл не найден.
    :raises ValueError: Формат данных CSV-файла некорректен или ошибка парсинга.
    :raises Exception: Не удалось прочитать CSV-файл.
    """

    try:
        data_frame = pd.read_csv(file_path, sep=";", dtype=str)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"CSV-файл пуст: {file_path}")
    except pd.errors.ParserError as exc:
        raise ValueError(f"Ошибка парсинга CSV-файла: {exc}")
    except Exception as exc:
        raise Exception(f"Не удалось прочитать CSV-файл: {exc}")

    return convert_data_to_transactions(data_frame)


def load_transactions_from_xlsx(file_path: str) -> list[dict[str, Any]]:
    """
    Загрузка транзакций из XLSX-файла.
    :param file_path: Путь к XLSX-файлу.
    :return: Список транзакций.
    :raises FileNotFoundError: XLSX-файл не найден.
    :raises ValueError: Формат данных XLSX-файла некорректен.
    :raises Exception: Не удалось прочитать XLSX-файл.
    """

    try:
        data_frame = pd.read_excel(file_path, dtype=str)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    except ValueError as exc:
        raise ValueError(f"Ошибка чтения XLSX-файла: {exc}")
    except Exception as exc:
        raise Exception(f"Не удалось прочитать XLSX-файл: {exc}")

    return convert_data_to_transactions(data_frame)


def convert_data_to_transactions(data_frame: pd.DataFrame) -> list[dict[str, Any]]:
    """
    Преобразование данных в список транзакций (словарей).
    :param data_frame: Данные транзакций в формате DataFrame.
    :return: Список транзакций.
    :raises ValueError: Формат данных некорректный.
    """
    # Удаляем строки, где все значения пустые (артефакты типа ';;;')
    data_frame = data_frame.dropna(how="all")

    # Удаляем строки с пустым идентификатором (id), если есть записи и строки с идентификатором
    if not data_frame.empty and "id" in data_frame.columns:
        data_frame = data_frame.dropna(subset=["id"])

    validate_dataframe(data_frame)

    records = data_frame.to_dict(orient="records")

    if not isinstance(records, list):
        raise ValueError("Ошибка конвертации данных: ожидался список словарей")

    # Инициализация списка транзакций (словарей)
    converted: list[dict[str, Any]] = []

    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Ошибка конвертации данных: Каждый элемент должен быть словарём")

        converted.append(convert_record_to_transaction(record))

    return converted


def validate_dataframe(data_frame: pd.DataFrame) -> None:
    """
    Проверка DataFrame на содержание данных и необходимых колонок.
    :raises ValueError: Отсутствуют обязательные колонки или данные отсутствуют.
    """
    if data_frame is None or data_frame.empty:
        raise ValueError("Данные отсутствуют: не удалось прочитать ни одной записи")

    missing = [col for col in REQUIRED_COLUMNS if col not in data_frame.columns]

    if missing:
        raise ValueError(f"В файле отсутствуют обязательные колонки: {missing}")


def convert_record_to_transaction(record: dict[Hashable, Any]) -> dict[str, Any]:
    """
    Преобразует исходную запись из данных в требуемый формат транзакции.
    :param record: Словарь с исходными полями из данных.
    :return: Словарь в целевом формате транзакции.
    """
    # Примечание: наименование валюты будет как и её код
    currency = str(record.get("currency_code") or "").strip()

    result: dict[str, Any] = {
        "id": int(record["id"]),
        "state": str(record.get("state") or ""),
        "date": str(record.get("date") or ""),
        "operationAmount": {
            "amount": str(record.get("amount") or ""),
            "currency": {
                "name": currency,
                "code": currency
            }
        },
        "description": str(record.get("description") or ""),
        "from": str(record.get("from") or ""),
        "to": str(record.get("to") or "")
    }

    return result
