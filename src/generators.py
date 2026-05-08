import textwrap
from typing import Iterator


def filter_by_currency(transaction_list: list[dict], currency: str) -> Iterator[dict]:
    """
    Получение транзакций для указанной валюты
    :param transaction_list: Список транзакций
    :param currency: Валюта
    :return: Итератор транзакций с указанной валютой
    """
    return (
        transaction
        for transaction in transaction_list
        if transaction["operationAmount"]["currency"]["code"] == currency
    )


def transaction_descriptions(transaction_list: list[dict]) -> Iterator[dict]:
    """
    Получение описаний транзакций
    :param transaction_list: Список транзакций
    :return: Генератор описаний транзакций
    """
    descriptions = [transaction["description"] for transaction in transaction_list]

    for description in descriptions:
        yield description


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Получить номера карт в указанном диапазоне
    :param start: Стартовое (минимальное) значение
    :param stop: Конечное (максимальное) значение
    :return: Генератор номеров карт в указанном диапазоне
    """
    if start < 0 or stop < 0:
        raise ValueError("Входные значения не могут быть отрицательными числами")

    if start > stop:
        raise ValueError("Стартовое значение не может быть больше конечного значения")

    if stop > 9999999999999999:
        raise ValueError("Конечное число не должно превышать \'9999 9999 9999 9999\' (16 цифр \'9\')")

    for number in range(start, stop + 1):
        number_as_string = str(number).zfill(16)
        splitted_number = textwrap.wrap(number_as_string, width=4)

        yield " ".join(splitted_number)
