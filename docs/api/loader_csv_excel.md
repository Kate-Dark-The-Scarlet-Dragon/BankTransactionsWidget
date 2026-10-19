# Модуль: `loader_csv_excel.py`

*Сгенерировано: 2026-10-20 01:12:03*

---

<div id="load_transactions_from_csv"></div>

## load_transactions_from_csv

**Тип:** function

**Кратко:** Загрузка транзакций из CSV-файла.

### Полная документация

```python
Загрузка транзакций из CSV-файла.
:param file_path: Путь к CSV-файлу.
:return: Список транзакций.
:raises FileNotFoundError: CSV-файл не найден.
:raises ValueError: Формат данных CSV-файла некорректен или ошибка парсинга.
:raises Exception: Не удалось прочитать CSV-файл.
```

---

<div id="load_transactions_from_xlsx"></div>

## load_transactions_from_xlsx

**Тип:** function

**Кратко:** Загрузка транзакций из XLSX-файла.

### Полная документация

```python
Загрузка транзакций из XLSX-файла.
:param file_path: Путь к XLSX-файлу.
:return: Список транзакций.
:raises FileNotFoundError: XLSX-файл не найден.
:raises ValueError: Формат данных XLSX-файла некорректен.
:raises Exception: Не удалось прочитать XLSX-файл.
```

---

<div id="convert_data_to_transactions"></div>

## convert_data_to_transactions

**Тип:** function

**Кратко:** Преобразование данных в список транзакций (словарей).

### Полная документация

```python
Преобразование данных в список транзакций (словарей).
:param data_frame: Данные транзакций в формате DataFrame.
:return: Список транзакций.
:raises ValueError: Формат данных некорректный.
```

---

<div id="validate_dataframe"></div>

## validate_dataframe

**Тип:** function

**Кратко:** Проверка DataFrame на содержание данных и необходимых колонок.

### Полная документация

```python
Проверка DataFrame на содержание данных и необходимых колонок.
:raises ValueError: Отсутствуют обязательные колонки или данные отсутствуют.
```

---

<div id="convert_record_to_transaction"></div>

## convert_record_to_transaction

**Тип:** function

**Кратко:** Преобразует исходную запись из данных в требуемый формат транзакции.

### Полная документация

```python
Преобразует исходную запись из данных в требуемый формат транзакции.
:param record: Словарь с исходными полями из данных.
:return: Словарь в целевом формате транзакции.
```

---

