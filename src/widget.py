import re
from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def is_only_cyrillic(text: str) -> bool:
    """
    Проверка, что текст состоит только из кириллических букв
    :param text: Текст
    :return: Признак - текст состоит только из кириллических букв
    """
    if len(text) == 0:
        raise ValueError("Невозможно выполнить проверку для пустой строки")

    return bool(re.search(r"^[а-яА-ЯёЁ\s]+$", text))


def mask_account_card(account_card: str) -> str:
    """
    Функция, которая форматирует номер в наименовании карты/счёта и выводит маску
    :param account_card: Наименование карты/счёта
    :return: Маска наименования карты/счёта
    """
    if len(account_card) == 0:
        raise ValueError("Невозможно выполнить операцию для пустого номера карты/счёта")

    parts = account_card.split()
    number = parts[-1]

    if is_only_cyrillic(parts[0]):
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{' '.join(parts[:-1])} {masked_number}"


def get_date(iso_date_time: str) -> str:
    """
    Получение даты из строки формата ISO 8601
    :param iso_date_time: Строка даты и времени в формате ISO 8601
    :return: Строка с датой в формате 'ДД.ММ.ГГГГ'
    """
    if len(iso_date_time) == 0:
        raise ValueError("Невозможно преобразовать дату из пустой строки")

    date_time = datetime.fromisoformat(iso_date_time)

    return date_time.strftime("%d.%m.%Y")
