def get_mask_card_number(card_number: int) -> str:
    """Функция, которая форматирует номер карты и выводит маску"""
    card_number_str = str(card_number)

    card_parts = [card_number_str[i : i + 4] for i in range(0, len(card_number_str), 4)]

    masked_card_number = f"{card_parts[0]} {card_parts[1][:2]}** **** {card_parts[-1]}"

    return masked_card_number


def get_mask_account(account_number: int) -> str:
    """Функция, которая форматирует номер лицевого счёта и выводит маску"""
    account_number_str = str(account_number)

    account_last_numbers = account_number_str[-4:]

    masked_account_number = f"**{account_last_numbers}"

    return masked_account_number
