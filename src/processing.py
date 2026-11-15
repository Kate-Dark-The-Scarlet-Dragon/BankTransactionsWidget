import re

from collections import Counter
from typing import Any


ALLOWED_STATES = ["EXECUTED", "CANCELED", "PENDING"]


def filter_by_state(operation_list: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """
    Фильтрация операций по их типу.
    :param operation_list: Список операций.
    :param state: Тип операции. По умолчанию - 'EXECUTED' (выполнено).
    :return: Список операций указанного типа.
    """
    if len(operation_list) == 0:
        return []

    filtered_operation_list = [operation for operation in operation_list if operation["state"] == state]

    return filtered_operation_list


def sort_by_date(operation_list: list[dict[str, Any]], descending: bool = True) -> list[dict[str, Any]]:
    """
    Сортировка операций по дате.
    :param operation_list: Список операций.
    :param descending: Признак - сортировка по убыванию. По умолчанию - True (да).
    :return: Отсортированный по дате список операций.
    """
    if len(operation_list) == 0:
        return []

    sorted_operation_list = sorted(operation_list, key=lambda x: x["date"], reverse=descending)

    return sorted_operation_list


def filter_by_description(operation_list: list[dict[str, Any]], search: str) -> list[dict[str, Any]]:
    """
    Фильтрация операций по описанию.
    :param operation_list: Список операций.
    :param search: Искомая строка в описании операции.
    :return: Список операций, в описании которых содержится искомая строка.
    """
    if len(operation_list) == 0:
        return []

    result = [
        operation
        for operation in operation_list
        if re.search(search, operation["description"], flags=re.I) is not None
    ]

    return result


def count_operations_by_category(operation_list: list[dict], categories: list[str]) -> dict[str, int]:
    """
    Подсчёт количества операций по каждой категории.
    :param operation_list: Список операций.
    :param categories: Список категорий операций (категории указаны в поле 'description').
    :return: Словарь с количеством категорий в списке операций.
    """
    # Получить список описаний операций в соответствии с указанными категориями
    descriptions = [
        operation.get("description")
        for operation in operation_list
        if operation.get("description") is not None
           and operation.get("description") in categories
    ]

    # Подсчёт категорий
    counter = Counter(descriptions)

    # Формирование словаря из категорий и их количества
    return {category: counter.get(category, 0) for category in categories}
