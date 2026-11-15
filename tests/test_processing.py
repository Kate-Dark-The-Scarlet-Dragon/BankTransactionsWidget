import pytest

from src import processing


#==============================================
#=== Тесты - Фильтрация операций по их типу ===
#==============================================

def test_filter_by_state(operation_list, filter_result_executed, filter_result_canceled):
    """Проверка результата фильтрации."""
    assert processing.filter_by_state(operation_list) == filter_result_executed
    assert processing.filter_by_state(operation_list, "CANCELED") == filter_result_canceled


def test_filter_by_state_with_empty_list():
    """Проверка на пустом списке."""
    assert processing.filter_by_state([]) == []


#===========================================
#=== Тесты - Сортировка операций по дате ===
#===========================================

def test_sort_by_date(operation_list, sort_result_asc, sort_result_desc):
    """Проверка результата сортировки."""
    assert processing.sort_by_date(operation_list, False) == sort_result_asc
    assert processing.sort_by_date(operation_list) == sort_result_desc


def test_sort_by_date_with_empty_list():
    """Проверка на пустом списке."""
    assert processing.sort_by_date([]) == []


#===============================================
#=== Тесты - Фильтрация операций по описанию ===
#===============================================

def test_empty_list_returns_empty():
    """Проверка на пустом списке."""
    assert processing.filter_by_description([], "Перевод") == []


@pytest.mark.parametrize(
    "search, expected_ids",
    [
        ("Перевод организации", [939719570, 594226727]),                      # Точная фраза - 2 значения
        ("с карты", [895315941]),                                             # Подстрока - 1 значение
        ("Перевод", [939719570, 142264268, 873106923, 895315941, 594226727]), # Подстрока - 4 значения
        ("СЧЕТА", [142264268, 873106923]),                                    # Регистронезависимость
        ("ипотека", []),                                                      # Нет совпадений
        ("", [939719570, 142264268, 873106923, 895315941, 594226727])         # Пустая строка - все значения
    ]
)
def test_search_matches(transaction_list, search, expected_ids):
    """Проверка результата фильтрации."""
    result = processing.filter_by_description(transaction_list, search)

    assert [op["id"] for op in result] == expected_ids


def test_missing_description_key_raises():
    """Проверка на отсутствие ключа 'description'."""
    with pytest.raises(KeyError):
        processing.filter_by_description([{"id": 1}], "Перевод")

#===============================================================
#=== Тесты - Подсчёт количества операций по каждой категории ===
#===============================================================

def test_counts_by_category(transaction_list):
    """Основной контракт: подсчёт по нескольким категориям + нули для отсутствующих."""
    result = processing.count_operations_by_category(
        transaction_list,
        ["Перевод организации", "Перевод с карты на карту", "Несуществующая"]
    )
    assert result == {
        "Перевод организации": 2,
        "Перевод с карты на карту": 1,
        "Несуществующая": 0
    }


def test_empty_operations():
    """Проверка на пустом списке."""
    result = processing.count_operations_by_category([], ["Перевод организации"])
    assert result == {"Перевод организации": 0}


def test_case_sensitive(transaction_list):
    """Проверка на регистрозависимость."""
    result = processing.count_operations_by_category(transaction_list, ["перевод организации"])
    assert result == {"перевод организации": 0}
