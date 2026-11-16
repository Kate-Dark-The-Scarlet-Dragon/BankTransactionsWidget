import os
from typing import Any

from src.generators import filter_by_currency
from src.loader_csv_excel import load_transactions_from_csv, load_transactions_from_xlsx
from src.processing import ALLOWED_STATES, filter_by_description, filter_by_state, sort_by_date
from src.utils import load_transactions_from_file
from src.widget import get_date, mask_account_card, validate_account_card

FILE_QUESTION = """Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла"""

STATUS_QUESTION_PART = """Введите статус, по которому необходимо выполнить фильтрацию.
Доступные для фильтровки статусы:"""

FILES = {"1": "JSON", "2": "CSV", "3": "XLSX"}

ASC_DESC = ["ПО ВОЗРАСТАНИЮ", "ПО УБЫВАНИЮ"]


def parametrized_question(question: str, incorrect_answer_text: str = "", allowed_answers: list[str] = []) -> str:
    """
    Задать вопрос пользователю с указанными параметрами.
    :param question: Вопрос пользователю.
    :param incorrect_answer_text: Ответ программы при некорректном вводе ответа пользователя.
    :param allowed_answers: Список допустимых ответов для пользователя.
    :return: Ответ пользователя.
    """
    if not incorrect_answer_text:
        incorrect_answer_text = "Тип сортировки"

    if not allowed_answers:
        allowed_answers = ["ДА", "НЕТ"]

    while True:
        print(f"\nПрограмма: {question}")
        choice = input("\nПользователь: ").strip()

        if choice.upper() in allowed_answers:
            return choice

        print(f'\nПрограмма: {incorrect_answer_text} "{choice!r}" недоступен.')


def load_operations(file_format: str) -> list[dict[str, Any]]:
    """
    Загрузка операций из указанного файла.
    :param file_format: Выбранный тип файла операций.
    :return: Список операций.
    :raises Exception: Указан неподдерживаемый формат файла.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))

    match file_format:
        case "JSON":
            json_file_path = os.path.join(base_dir, "data", "operations.json")

            return load_transactions_from_file(json_file_path)

        case "CSV":
            csv_file_path = os.path.join(base_dir, "data", "transactions.csv")

            return load_transactions_from_csv(csv_file_path)

        case "XLSX":
            excel_file_path = os.path.join(base_dir, "data", "transactions_excel.xlsx")

            return load_transactions_from_xlsx(excel_file_path)

        case _:
            raise Exception(f"Обнаружен неподдерживаемый формат файла: {file_format}")


def print_operations_to_console(operation_list: list[dict[str, Any]]) -> None:
    """
    Вывод банковских операций в консоль.
    :param operation_list: Список банковских операций для вывода.
    """
    if not operation_list or len(operation_list) == 0:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print("\nПрограмма: Распечатываю итоговый список транзакций...")
    print(f"\nПрограмма:\nВсего банковских операций в выборке: {len(operation_list)}\n")

    for operation in operation_list:
        # Вывод даты и описания операции
        date = get_date(operation["date"])

        print(f"{date} {operation["description"]}")

        # Вывод движения денежных средств
        destination = mask_account_card(operation["to"])

        if "from" in operation.keys() and validate_account_card(operation.get("from", "")):
            source = mask_account_card(operation["from"])

            print(f"{source} -> {destination}")
        else:
            print(destination)

        # Вывод суммы операции
        amount = operation["operationAmount"]["amount"]
        currency = operation["operationAmount"]["currency"]["name"]

        print(f"Сумма: {amount} {currency}")
        print()


def main() -> None:
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # 1. Выбор файла для загрузки транзакций
    selected_menu_item = parametrized_question(FILE_QUESTION, "Выбранный пункт меню", list(FILES.keys()))

    file_format = FILES[selected_menu_item]

    print(f"\nПрограмма: Для обработки выбран {file_format}-файл.")

    operations = load_operations(file_format)

    # 2. Выбор статуса транзакций
    status_question = f"{STATUS_QUESTION_PART} {", ".join(ALLOWED_STATES)}"

    selected_state = parametrized_question(status_question, "Статус операции", ALLOWED_STATES).upper()

    operations = filter_by_state(operations, selected_state)

    print(f'\nПрограмма: Операции отфильтрованы по статусу "{selected_state}"')

    # 3. Выбор - нужна ли сортировка операций по датам
    sort_by_date_answer = parametrized_question("Отсортировать операции по дате? Да/Нет")

    if sort_by_date_answer.upper() == "ДА":
        # 3.1. Выбор направления сортировки операций по датам
        sorting_direction_answer = parametrized_question(
            "Отсортировать по возрастанию или по убыванию?", allowed_answers=ASC_DESC
        )

        sort_desc = sorting_direction_answer.upper() == "ПО УБЫВАНИЮ"

        operations = sort_by_date(operations, sort_desc)

    # 4. Выбор - выводить ли только рублёвые транзакции
    filter_by_rub_answer = parametrized_question("Выводить только рублевые транзакции? Да/Нет")

    if filter_by_rub_answer.upper() == "ДА":
        operations = list(filter_by_currency(operations, "RUB"))

    # 5. Выбор - нужна ли фильтрация операций по слову в описании
    filter_by_word_answer = parametrized_question(
        "Отфильтровать список транзакций по определенному слову в описании? Да/Нет"
    )

    if filter_by_word_answer.upper() == "ДА":
        # 5.1. Выбор слова для фильтрации по описаниям операций
        print("\nПрограмма: Введите слово для поиска в описании транзакций")
        filter_text = input("\nПользователь: ").strip()

        operations = filter_by_description(operations, filter_text)

    # 6. Вывод результата
    print_operations_to_console(operations)


if __name__ == "__main__":
    main()
