import re
from datetime import datetime

from src import masks


def is_cyrillic(text: str) -> bool:
    """Проверка, что текст состоит из кириллических букв"""

    return bool(re.search("[а-яА-ЯёЁ]", text))


def mask_account_card(account_card: str) -> str:
    """Функция, которая форматирует номер в наименовании карты/счёта и выводит маску"""

    parts = account_card.split()
    number = int(parts[-1])

    masked_number = ""

    if is_cyrillic(parts[0]):
        masked_number = masks.get_mask_account(number)
    else:
        masked_number = masks.get_mask_card_number(number)

    return f"{' '.join(parts[:-1])} {masked_number}"


def get_date(iso_date_time: str) -> str:
    """Получение даты в формате 'ДД.ММ.ГГГГ' из строки формата даты и времени ISO 8601"""

    date_time = datetime.fromisoformat(iso_date_time)

    return date_time.strftime("%d.%m.%Y")
