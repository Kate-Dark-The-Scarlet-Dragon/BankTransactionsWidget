def filter_by_state(operation_list: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Получение списка операций с указанным типом операции
    :param operation_list: Список операций
    :param state: Тип операции. По умолчанию - 'EXECUTED' (выполнено)
    :return: Список операций указанного типа
    """
    filtered_operation_list = [operation for operation in operation_list if operation["state"] == state]

    return filtered_operation_list
