import json
from src.external_api import convert_currency
from typing import Any


def load_transactions_from_file(file_path: str) -> list[dict[str, Any]]:
    """
    Загрузка списка транзакций (операций) из JSON-файла.
    :param file_path: Путь к JSON-файлу
    :return:  Список транзакций (операций).
    Если файл не найден, пустой, повреждён, не может быть прочитан или содержит не список словарей,
    то возвращается пустой список.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, PermissionError, FileNotFoundError, json.JSONDecodeError):
        # Файл не может быть прочитан, не найден или повреждён
        return []

    # Проверка, что данные являются списком словарей
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        return data

    return []


def get_transaction_amount_in_rub(transaction: dict[str, Any]) -> float:
    """
    Получить сумму транзакции в рублях.
    Если валюта в транзакции в долларах ("USD") или в евро ("EUR")
    – идёт обращение к внешнему API для конвертации суммы.

    :param transaction: Данные транзакции.
    :return: Сумма в рублях.
    :raise KeyError: Отсутствуют обязательные поля в теле транзакции.
    :raise ValueError: Неизвестный код валюты.
    :raise Exception: При ошибке конвертации через API.
    """
    operation_amount = transaction["operationAmount"]
    amount_str = operation_amount["amount"]
    currency_code = str(operation_amount["currency"]["code"])

    amount = float(amount_str)

    if currency_code == "RUB":
        return amount

    if currency_code in ("USD", "EUR"):
        return convert_currency(amount, currency_code, "RUB")

    raise ValueError(f"Не удалось распознать код валюты: {currency_code}")
