from src import processing


def test_filter_by_state(operation_list, filter_result_executed, filter_result_canceled):
    assert processing.filter_by_state(operation_list) == filter_result_executed
    assert processing.filter_by_state(operation_list, "CANCELED") == filter_result_canceled


def test_filter_by_state_with_empty_list():
    assert processing.filter_by_state([]) == []


def test_sort_by_date(operation_list, sort_result_asc, sort_result_desc):
    assert processing.sort_by_date(operation_list, False) == sort_result_asc
    assert processing.sort_by_date(operation_list) == sort_result_desc


def test_sort_by_date_with_empty_list():
    assert processing.sort_by_date([]) == []
