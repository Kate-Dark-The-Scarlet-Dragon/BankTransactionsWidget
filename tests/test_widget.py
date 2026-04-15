import pytest

from src import widget


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Текст", True),
        ("Текст текст", True),
        ("Text", False),
        ("Текст text", False),
        ("1234567890", False),
        ("Текст 1234", False)
    ]
)
def test_is_cyrillic_with_different_texts(text, expected):
    assert widget.is_only_cyrillic(text) == expected


def test_is_cyrillic_with_empty_string():
    with pytest.raises(ValueError) as exception_info:
        widget.is_only_cyrillic("")

    assert str(exception_info.value) == "Невозможно выполнить проверку для пустой строки"


@pytest.mark.parametrize(
    "account_card, expected",
    [
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Счёт 35383033474447895560", "Счёт **5560"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658")
    ]
)
def test_mask_account_card_with_correct_number(account_card, expected):
    assert widget.mask_account_card(account_card) == expected


def test_mask_account_card_with_empty_string():
    with pytest.raises(ValueError) as exception_info:
        widget.mask_account_card("")

    assert str(exception_info.value) == "Невозможно выполнить операцию для пустого номера карты/счёта"


@pytest.mark.parametrize(
    "iso_date_time, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("1992-11-25T15:08:46.230871", "25.11.1992")
    ]
)
def test_get_date(iso_date_time, expected):
    assert widget.get_date(iso_date_time) == expected


def test_get_date_with_empty_string():
    with pytest.raises(ValueError) as exception_info:
        widget.get_date("")

    assert str(exception_info.value) == "Невозможно преобразовать дату из пустой строки"
