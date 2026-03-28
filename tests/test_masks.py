import pytest

from src import masks


@pytest.fixture
def incorrect_numbers():
    return ["1242", "123456789012345678" "sometext", "sometext1234", "*-&?"]


@pytest.mark.parametrize(
    "number, expected",
    [
        ("1596837868705199", "1596 83** **** 5199"),
        ("7158300734726758", "7158 30** **** 6758"),
        ("5999414228426353", "5999 41** **** 6353"),
    ]
)
def test_get_mask_card_number_with_correct_number(number, expected):
    assert masks.get_mask_card_number(number) == expected


def test_get_mask_card_number_with_no_number():
    with pytest.raises(ValueError) as exception_info:
        masks.get_mask_card_number("")

    assert str(exception_info.value) == "Отсутствует номер карты"


def test_get_mask_card_number_with_incorrect_number(incorrect_numbers):
    for incorrect_number in incorrect_numbers:
        with pytest.raises(ValueError) as exception_info:
            masks.get_mask_card_number(incorrect_number)

        assert str(exception_info.value) == "Номер карты должен состоять из 16 цифр"


@pytest.mark.parametrize(
    "number, expected",
    [
        ("64686473678894779589", "**9589"),
        ("35383033474447895560", "**5560"),
        ("73654108430135874305", "**4305")
    ]
)
def test_get_mask_account_with_correct_number(number, expected):
    assert masks.get_mask_account(number) == expected


def test_get_mask_account_with_no_number():
    with pytest.raises(ValueError) as exception_info:
        masks.get_mask_account("")

    assert str(exception_info.value) == "Отсутствует номер лицевого счёта"


def test_get_mask_account_with_incorrect_number(incorrect_numbers):
    for incorrect_number in incorrect_numbers:
        with pytest.raises(ValueError) as exception_info:
            masks.get_mask_account(incorrect_number)

        assert str(exception_info.value) == "Номер лицевого счёта состоять из 20 цифр"
