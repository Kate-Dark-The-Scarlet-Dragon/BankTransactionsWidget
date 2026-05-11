import os
import requests


def convert_currency(amount: float, from_currency: str, to_currency: str = "RUB") -> float:
    """
    Конвертация суммы из одной валюты в другую через внешнее API.
    :param amount: Сумма для конвертации.
    :param from_currency: Трёхбуквенный код исходной валюты.
    :param to_currency: Трёхбуквенный код целевой валюты (по умолчанию в рублях - RUB).
    :return: Сконвертированная сумма в целевой валюте.
    :raise Exception: Запрос к API завершился ошибкой или ответ не содержит "success = true".
    """
    api_key = os.getenv("EXCHANGE_API_KEY")

    if not api_key:
        raise Exception("API key для Exchange Rates Data не найден. Установите переменную окружения EXCHANGE_API_KEY")

    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {"apikey": api_key}
    params: dict[str, str|float] = {"to": to_currency, "from": from_currency, "amount": amount}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)

        response.raise_for_status() # Проброс исключения при статусе 4xx/5xx

        data = response.json()

        if not data.get("success", False):
            get_error_message = data.get("error", {}).get("info", "Неизвестная ошибка API")

            raise Exception(f"Ошибка API: {get_error_message}")

        result = data.get("result")

        if result is None:
            raise Exception("В ответе API отсутствует поле 'result'")

        return float(result)

    except requests.exceptions.RequestException as e:
        error_message = f"Ошибка при обращении к API конвертации валют: {e}"

        print(error_message)

        raise Exception(error_message)

    except Exception as e:
        print(f"Ошибка конвертации: {e}")

        raise
