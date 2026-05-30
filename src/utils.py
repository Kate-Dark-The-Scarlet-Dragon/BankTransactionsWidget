import json
from typing import Any

from src.external_api import convert_currency
from src.logger_setup import setup_logger

# Настройка логгера
logger = setup_logger(__name__)


def load_transactions_from_file(file_path: str) -> list[dict[str, Any]]:
    """
    Загрузка списка транзакций (операций) из JSON-файла.
    :param file_path: Путь к JSON-файлу
    :return:  Список транзакций (операций).
    Если файл не найден, пустой, повреждён, не может быть прочитан или содержит не список словарей,
    то возвращается пустой список.
    """
    logger.info(f"Запуск загрузки транзакций из файла: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, PermissionError, FileNotFoundError, json.JSONDecodeError) as e:
        # Файл не может быть прочитан, не найден или повреждён
        logger.error(f"Ошибка при загрузке транзакций: {e}")

        return []

    # Проверка, что данные являются списком словарей
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        logger.info(f"Завершена загрузка транзакций из файла: {file_path}")

        return data

    logger.warning(f'Отсутствуют данные в файле "{file_path}" либо их формат не соответствует формату транзакций')

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
    logger.info("Запуск получения суммы из транзакции")

    operation_amount = transaction["operationAmount"]
    amount_str = operation_amount["amount"]
    currency_code = str(operation_amount["currency"]["code"])

    amount = float(amount_str)

    if currency_code == "RUB":
        logger.info(f"Получена сумма транзакции в рублях: {currency_code}")

        return amount

    if currency_code in ("USD", "EUR"):
        logger.info(f'Запуск конвертации суммы транзакции из валюты "{currency_code}"')

        try:
            amount = convert_currency(amount, currency_code, "RUB")

            logger.info(f'Завершена конвертация суммы транзакции из валюты "{currency_code}" в рубли: {amount}')

            return amount
        except Exception as e:
            logger.error(f"Ошибка при конвертации суммы в транзакции: {e}")

            raise e

    logger.error(f"Неизвестная валюта в транзакции: {currency_code}")

    raise ValueError(f"Не удалось распознать код валюты: {currency_code}")
