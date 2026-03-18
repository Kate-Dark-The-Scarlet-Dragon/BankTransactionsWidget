from src import masks
import re


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
