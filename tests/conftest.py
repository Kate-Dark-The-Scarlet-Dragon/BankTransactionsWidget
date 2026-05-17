import pytest


# Фикстура списка некорректных номеров карт
@pytest.fixture
def incorrect_numbers():
    return ["1242", "123456789012345678" "sometext", "sometext1234", "*-&?"]


# Фикстуры списков операций
@pytest.fixture
def operation_list():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"}
    ]


@pytest.fixture
def filter_result_executed():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}
    ]


@pytest.fixture
def filter_result_canceled():
    return [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"}
    ]


@pytest.fixture
def sort_result_asc():
    return [
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}
    ]


@pytest.fixture
def sort_result_desc():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}
    ]
# endregion


# Фикстуры списков транзакций
@pytest.fixture
def transaction_list():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount":
                {
                    "amount": "9824.07",
                    "currency":
                        {
                            "name": "USD",
                            "code": "USD"
                        }
                },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount":
                {
                    "amount": "79114.93",
                    "currency":
                        {
                            "name": "USD",
                            "code": "USD"
                        }
                },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount":
                {
                    "amount": "43318.34",
                    "currency":
                        {
                            "name": "руб.",
                            "code": "RUB"
                        }
                },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount":
                {
                    "amount": "56883.54",
                    "currency":
                        {
                            "name": "USD",
                            "code": "USD"
                        }
                },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount":
                {
                    "amount": "67314.70",
                    "currency":
                        {
                            "name": "руб.",
                            "code": "RUB"
                        }
                },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]


@pytest.fixture
def transaction_list_filtered_by_rub():
    return [
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount":
                {
                    "amount": "43318.34",
                    "currency":
                        {
                            "name": "руб.",
                            "code": "RUB"
                        }
                },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount":
                {
                    "amount": "67314.70",
                    "currency":
                        {
                            "name": "руб.",
                            "code": "RUB"
                        }
                },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]


@pytest.fixture
def transaction_list_filtered_by_usd():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount":
                {
                    "amount": "9824.07",
                    "currency":
                        {
                            "name": "USD",
                            "code": "USD"
                        }
                },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount":
                {
                    "amount": "79114.93",
                    "currency":
                        {
                            "name": "USD",
                            "code": "USD"
                        }
                },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount":
                {
                    "amount": "56883.54",
                    "currency":
                        {
                            "name": "USD",
                            "code": "USD"
                        }
                },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        }
    ]
# endregion


# Фикстуры списков описаний транзакций
@pytest.fixture
def transaction_description_list():
    return [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации"
    ]


# region Фикстуры списков сгенерированных номеров карт
@pytest.fixture
def card_numbers_16_to_21():
    return [
        "0000 0000 0000 0016",
        "0000 0000 0000 0017",
        "0000 0000 0000 0018",
        "0000 0000 0000 0019",
        "0000 0000 0000 0020",
        "0000 0000 0000 0021"
    ]


@pytest.fixture
def card_numbers_5_last_to_max():
    return [
        "9999 9999 9999 9995",
        "9999 9999 9999 9996",
        "9999 9999 9999 9997",
        "9999 9999 9999 9998",
        "9999 9999 9999 9999"
    ]
# endregion


# region Фикстуры транзакции в разных валютах
@pytest.fixture
def usd_transaction():
    return {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount":
            {
                "amount": "9824.07",
                "currency":
                    {
                        "name": "USD",
                        "code": "USD"
                    }
            },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    }


@pytest.fixture
def rub_transaction():
    return {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount":
            {
                "amount": "1500.50",
                "currency":
                    {
                        "name": "руб.",
                        "code": "RUB"
                    }
            },
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657"
    }


@pytest.fixture
def eur_transaction():
    return {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount":
            {
                "amount": "100.00",
                "currency":
                    {
                        "name": "EUR",
                        "code": "EUR"
                    }
            },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188"
    }


@pytest.fixture
def incorrect_currency_transaction():
    return {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount":
            {
                "amount": "56883.54",
                "currency":
                    {
                        "name": "",
                        "code": "TTT"
                    }
            },
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229"
    }
# endregion
