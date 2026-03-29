def filter_by_state(operation_list: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Получение списка операций с указанным типом операции
    :param operation_list: Список операций
    :param state: Тип операции. По умолчанию - 'EXECUTED' (выполнено)
    :return: Список операций указанного типа
    """
    if len(operation_list) == 0:
        return operation_list

    filtered_operation_list = [operation for operation in operation_list if operation["state"] == state]

    return filtered_operation_list


def sort_by_date(operation_list: list[dict], descending: bool = True) -> list[dict]:
    """
    Сортировка операций по дате
    :param operation_list: Список операций
    :param descending: Признак - сортировка по убыванию. По умолчанию - True (да)
    :return: Отсортированный по дате список операций
    """
    if len(operation_list) == 0:
        return operation_list

    sorted_operation_list = sorted(operation_list, key=lambda x: x["date"], reverse=descending)

    return sorted_operation_list
