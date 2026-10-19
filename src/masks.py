from src.logger_setup import setup_logger

# Настройка логгера
logger = setup_logger(__name__)


def get_mask_card_number(card_number: str) -> str:
    """
    Функция, которая форматирует номер карты и выводит маску
    :param card_number: Номер карты
    :return: Маска номера карты
    """
    logger.info(f"Запуск наложения маски для номера карты: {card_number}")

    if len(card_number) == 0:
        error_message = "Отсутствует номер карты"

        logger.error(error_message)

        raise ValueError(error_message)

    if len(card_number) != 16 or not card_number.isdecimal():
        error_message = "Номер карты должен состоять из 16 цифр"

        logger.error(error_message)

        raise ValueError(error_message)

    card_parts = [card_number[i : i + 4] for i in range(0, len(card_number), 4)]

    masked_card_number = f"{card_parts[0]} {card_parts[1][:2]}** **** {card_parts[-1]}"

    logger.info(f"Сформирована маска для номера карты: {card_number}")

    return masked_card_number


def get_mask_account(account_number: str) -> str:
    """
    Функция, которая форматирует номер лицевого счёта и выводит маску
    :param account_number: Номер лицевого счёта
    :return: Маска номера лицевого счёта
    """
    logger.info(f"Запуск наложения маски для номера лицевого счёта: {account_number}")

    if len(account_number) == 0:
        error_message = "Отсутствует номер лицевого счёта"

        logger.error(error_message)

        raise ValueError(error_message)

    if len(account_number) != 20 or not account_number.isdecimal():
        error_message = "Номер лицевого счёта состоять из 20 цифр"

        logger.error(error_message)

        raise ValueError(error_message)

    account_last_numbers = account_number[-4:]

    masked_account_number = f"**{account_last_numbers}"

    logger.info(f"Сформирована маска для номера лицевого счёта: {account_number}")

    return masked_account_number
