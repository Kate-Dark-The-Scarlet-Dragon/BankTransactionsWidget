import re
from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number

ACCOUNT_CARD_PATTERN = r"^(?:[A-ZА-Я](?:[A-ZА-Я]|[a-zа-я])*(?:\s[A-ZА-Я](?:[A-ZА-Я]|[a-zа-я])*)?)\s(?:\d{16}|\d{20})$"


def validate_account_card(account_card: str) -> bool:
    """
    Проверка формата наименования счёта/карты.
    :param account_card: Наименование карты/счёта.
    :return: Наименование счёта/карты корректно.
    """
    return bool(re.fullmatch(ACCOUNT_CARD_PATTERN, account_card))


def mask_account_card(account_card: str) -> str:
    """
    Формирование маски для наименований карты/счёта.
    :param account_card: Наименование карты/счёта.
    :return: Маска наименования карты/счёта.
    :raises ValueError: Не удалось определить по наименованию к какому типу относится номер - счёт или карта.
    """
    if len(account_card) == 0:
        raise ValueError("Невозможно выполнить операцию для пустого номера карты/счёта")

    parts = account_card.split()
    number = parts[-1]
    masked_number = ""

    match len(number):
        case 16:
            masked_number = get_mask_card_number(number)
        case 20:
            masked_number = get_mask_account(number)
        case _:
            raise ValueError(f"Не удалось определить тип (карта или счёт) в наименовании: {account_card}")

    return f"{' '.join(parts[:-1])} {masked_number}"


def get_date(iso_date_time: str) -> str:
    """
    Получение даты из строки формата ISO 8601.
    :param iso_date_time: Строка даты и времени в формате ISO 8601.
    :return: Строка с датой в формате 'ДД.ММ.ГГГГ'.
    """
    if len(iso_date_time) == 0:
        raise ValueError("Невозможно преобразовать дату из пустой строки")

    date_time = datetime.fromisoformat(iso_date_time)

    return date_time.strftime("%d.%m.%Y")
