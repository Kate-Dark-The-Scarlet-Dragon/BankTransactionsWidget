def get_mask_card_number(card_number: str) -> str:
    """
    Функция, которая форматирует номер карты и выводит маску
    :param card_number: Номер карты
    :return: Маска номера карты
    """
    if len(card_number) == 0:
        raise ValueError("Отсутствует номер карты")

    if len(card_number) != 16 or card_number.isdecimal():
        raise ValueError("Номер карты должен состоять из 16 цифр")

    card_parts = [card_number[i : i + 4] for i in range(0, len(card_number), 4)]

    masked_card_number = f"{card_parts[0]} {card_parts[1][:2]}** **** {card_parts[-1]}"

    return masked_card_number


def get_mask_account(account_number: str) -> str:
    """
    Функция, которая форматирует номер лицевого счёта и выводит маску
    :param account_number: Номер лицевого счёта
    :return: Маска номера лицевого счёта
    """
    if len(account_number) == 0:
        raise ValueError("Отсутствует номер лицевого счёта")

    if len(account_number) != 20 or account_number.isdecimal():
        raise ValueError("Номер лицевого счёта состоять из 20 цифр")

    account_last_numbers = account_number[-4:]

    masked_account_number = f"**{account_last_numbers}"

    return masked_account_number
