import pytest
from pytest_lazy_fixtures import lf

from src import processing


@pytest.mark.parametrize(
    "operations, state, expected",
    [
        (lf("operation_list"), "EXECUTED", lf("filter_result_executed")),
        (lf("operation_list"), "CANCELED", lf("filter_result_canceled")),
    ],
)
def test_filter_by_state(operations, state, expected):
    assert processing.filter_by_state(operations, state) == expected


def test_filter_by_state_with_empty_list():
    assert processing.filter_by_state([], "EXECUTED") == []


@pytest.mark.parametrize(
    "operations, is_descending, expected",
    [(lf("operation_list"), False, lf("sort_result_asc")), (lf("operation_list"), True, lf("sort_result_desc"))],
)
def test_sort_by_date(operations, is_descending, expected):
    assert processing.sort_by_date(operations, is_descending) == expected


def test_sort_by_date_with_empty_list():
    assert processing.filter_by_state([]) == []
