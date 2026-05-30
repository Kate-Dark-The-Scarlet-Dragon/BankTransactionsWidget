# Проект "Виджет банковских операций"

## Содержание
- [Описание](#описание)
- [Статус проекта](#статус-проекта)
- [Реализация](#реализация)
- [Установка](#установка)
- [Команда проекта](#команда-проекта)

## Описание
Данный проект создаётся в рамках обучения курса "Python-разработчик" онлайн-университета цифровых профессий SkyPro.
Это виджет, который показывает несколько последних успешных банковских операций клиента.

### Статус проекта:
В данный момент проект находится в статусе разработки.

### Реализация

Реализованы следующие модули:
- Модуль `decorators`:
  - [write_log_text](docs/api/decorators.md#write_log_text) - Логирование информации в консоль/файл;
  - [log](docs/api/decorators.md#log) - Декоратор для логирования вызовов функции;
- Модуль `external_api.py`:
  - [convert_currency](docs/api/external_api.md#convert_currency) - Конвертация суммы из одной валюты в другую через внешнее API;
- Модуль `generators`:
  - [filter_by_currency](docs/api/generators.md#filter_by_currency) - Получение транзакций для указанной валюты;
  - [transaction_descriptions](docs/api/generators.md#transaction_descriptions) - Получение описаний транзакций;
  - [card_number_generator](docs/api/generators.md#card_number_generator) - Получить номера карт в указанном диапазоне;
- Модуль `logger_setup.py`:
  - [setup_logger](docs/api/logger_setup.md#setup_logger) - Создание и настройка логгера для указанного модуля;
- Модуль `masks`:
  - [get_mask_card_number](docs/api/masks.md#get_mask_card_number) - Функция, которая форматирует номер карты и выводит маску;
  - [get_mask_account](docs/api/masks.md#get_mask_account) - Функция, которая форматирует номер лицевого счёта и выводит маску;
- Модуль `widget` - содержит функции:
  - наложение маски на номера, используя функции из модуля `masks`;
  - получение даты из строки даты-времени формата ISO 8601;
- Модуль `processing`:
  - [filter_by_state](docs/api/processing.md#filter_by_state) - Получение списка операций с указанным типом операции;
  - [sort_by_date](docs/api/processing.md#sort_by_date) - Сортировка операций по дате; 
- Модуль `utils`:
  - [load_transactions_from_file](docs/api/utils.md#load_transactions_from_file) - Загрузка списка транзакций (операций) из JSON-файла;
  - [get_transaction_amount_in_rub](docs/api/utils.md#get_transaction_amount_in_rub) - Получить сумму транзакции в рублях;
- Модуль `widget`:
  - [is_only_cyrillic](docs/api/widget.md#is_only_cyrillic) - Проверка, что текст состоит только из кириллических букв;
  - [mask_account_card](docs/api/widget.md#mask_account_card) - Функция, которая форматирует номер в наименовании карты/счёта и выводит маску;
  - [get_date](docs/api/widget.md#get_date) - Получение даты из строки формата ISO 8601.

> 📘 **Полная документация** с примерами и описанием параметров доступна в папке [`docs/api`](docs/api).

### Тестирование

Для запуска тестов в консоли введите команду:
```
pytest tests
```
## Установка:

1. Клонирование репозитория:
```
https://github.com/Kate-Dark-The-Scarlet-Dragon/BankTransactionsWidget.git
```
2. Установка Poetry:
```
pip install poetry
```
3. Установка зависимостей через Poetry:
```
poetry install
```

### 📊 Результаты покрытия тестами

```
📈 Покрытие кода:    Кол-во       Процент
                     тестов      покрытия
src\__init__.py           0          100%
src\decorators.py        26          100%
src\external_api.py      29          100%
src\generators.py        19          100%
src\logger_setup.py      27           81%
src\masks.py             30          100%
src\processing.py        10          100%
src\utils.py             38          100%
src\widget.py            21          100%
TOTAL                   200           98%
```

> 📊 **HTML отчёт покрытия**: [`htmlcov/index.html`](htmlcov/src/index.html)

## Команда проекта

- [Соловкина Екатерина](tg://resolve?domain=the_scarlet_dragon) - Back-End Engineer