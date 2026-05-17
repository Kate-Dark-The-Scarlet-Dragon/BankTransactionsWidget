from pathlib import Path

from src.masks import get_mask_account, get_mask_card_number
from src.utils import get_transaction_amount_in_rub, load_transactions_from_file


def main() -> None:
    print("=== Запуск демонстрации логирования ===")

    transaction = {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount":
            {
                "amount": "100.00",
                "currency":
                    {
                        "name": "EUR",
                        "code": "EUR"
                    }
            },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188"
    }

    # Обёртка на случай, если в каком-то из модулей прокинется исключение
    try:
        get_mask_card_number("5999414228426353")
        get_mask_account("35383033474447895560")
        load_transactions_from_file("data/operations.json")
        get_transaction_amount_in_rub(transaction)
    except Exception as e:
        print(f"При выполнении возникло исключение в одном из методов: {e}")

    print("\nЛоги записаны в папку logs/. Файлы:")

    for log_file in Path("logs").glob("*.log"):
        print(f"  - {log_file}")

    print("\n=== Демонстрации логирования завершена ===")


if __name__ == "__main__":
    main()
