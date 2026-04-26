import pytest

from src import generators


def test_filter_by_currency(transaction_list, transaction_list_filtered_by_rub, transaction_list_filtered_by_usd):
    result_by_rus = list(generators.filter_by_currency(transaction_list, "RUB"))
    result_by_usd = list(generators.filter_by_currency(transaction_list, "USD"))

    assert result_by_rus == transaction_list_filtered_by_rub
    assert result_by_usd == transaction_list_filtered_by_usd


def test_filter_by_currency_exception(transaction_list, transaction_list_filtered_by_rub):
    iterator = generators.filter_by_currency(transaction_list, "RUB")

    next(iterator)
    next(iterator)

    with pytest.raises(StopIteration):
        next(iterator)


def test_transaction_descriptions(transaction_list, transaction_description_list):
    result = list(generators.transaction_descriptions(transaction_list))

    assert result == transaction_description_list


def test_card_number_generator(card_numbers_16_to_21, card_numbers_5_last_to_max):
    result_16_to_21 = list(generators.card_number_generator(16, 21))
    result_5_last_to_max = list(generators.card_number_generator(9999999999999995, 9999999999999999))
    result_single_number = list(generators.card_number_generator(101, 101))

    assert result_16_to_21 == card_numbers_16_to_21
    assert result_5_last_to_max == card_numbers_5_last_to_max
    assert result_single_number == ["0000 0000 0000 0101"]


@pytest.mark.parametrize(
    "start, stop, expected_exception_text",
    [
        (-1, 21, "Входные значения не могут быть отрицательными числами"),
        (16, -3, "Входные значения не могут быть отрицательными числами"),
        (-1, -3, "Входные значения не могут быть отрицательными числами"),
        (21, 16, "Стартовое значение не может быть больше конечного значения"),
        (16, 10000000000000000, "Конечное число не должно превышать \'9999 9999 9999 9999\' (16 цифр \'9\')")
    ]
)
def test_card_number_generator_exceptions(start, stop, expected_exception_text):
    generator = generators.card_number_generator(start, stop)

    with pytest.raises(ValueError) as exception_info:
        list(generator)

    assert str(exception_info.value) == expected_exception_text
