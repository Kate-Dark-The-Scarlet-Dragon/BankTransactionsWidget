import logging
import os
from pathlib import Path

from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

LOG_MESSAGE_FORMAT = os.getenv("LOG_MESSAGE_FORMAT")
LOG_DATE_FORMAT = os.getenv("LOG_DATE_FORMAT")

if not LOG_MESSAGE_FORMAT:
    LOG_MESSAGE_FORMAT = "%(asctime)s %(filename)s %(levelname)s: %(message)s"

    print("Предупреждение: не найден LOG_MESSAGE_FORMAT в .env."
          f" Используется значение по умолчанию: \"{LOG_MESSAGE_FORMAT}\".")

if not LOG_DATE_FORMAT:
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    print("Предупреждение: не найден LOG_DATE_FORMAT в .env."
          f" Используется значение по умолчанию: \"{LOG_DATE_FORMAT}\".")

# Директория для логов (создаётся, если не существует)
LOG_DIRECTORY = Path("logs")

LOG_DIRECTORY.mkdir(exist_ok=True)


def setup_logger(module_name: str) -> logging.Logger:
    """
    Создание и настройка логгера для указанного модуля.
    Логи пишутся в файл "logs/<module_name>.log".
    При каждом запуске происходит перезапись файла.
    :param module_name: Наименование модуля
    """
    logger = logging.getLogger(module_name)

    logger.setLevel(logging.DEBUG)

    # Очистка от существующих обработчиков во избежание дублей при повторной настройке
    if logger.handlers:
        logger.handlers.clear()

    # Создание обработчика для записи в файл с перезаписью
    log_file = LOG_DIRECTORY / f"{module_name}.log"
    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")

    file_handler.setLevel(logging.DEBUG)

    # Установка форматирования с параметрами из .env
    formatter = logging.Formatter(LOG_MESSAGE_FORMAT, datefmt=LOG_DATE_FORMAT)

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
