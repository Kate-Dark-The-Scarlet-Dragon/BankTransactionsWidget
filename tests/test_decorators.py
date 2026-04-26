from pathlib import Path

import pytest

from config import BASE_DIRECTORY
from src.decorators import log


def test_log_console_success(capsys):
    @log()
    def some_func():
        return "some funct result"

    result = some_func()
    captured = capsys.readouterr()

    assert result == "some funct result"
    assert captured.out.strip() == "some_func ok"


def test_log_console_error(capsys):
    @log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(5, 0)

    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError. Inputs: (5, 0), {}" in captured.out


def test_log_console_with_kwargs(capsys):
    @log()
    def greet_user(name, greeting="Hello"):
        return f"{greeting}, {name}"

    result = greet_user("Kate", greeting="Hi")
    captured = capsys.readouterr()

    assert result == "Hi, Kate"
    assert captured.out.strip() == "greet_user ok"


def test_log_no_parentheses_console(capsys):
    @log()
    def get_none():
        return None

    get_none()
    captured = capsys.readouterr()

    assert "get_none ok" in captured.out


def test_log_file_success(capsys):
    log_file = Path(BASE_DIRECTORY) / "test.log"

    @log(filepath=str(log_file))
    def some_func():
        return "some funct result"

    result = some_func()

    assert result == "some funct result"

    # В консоль ничего не должно попасть
    captured = capsys.readouterr()

    assert captured.out == ""

    # Проверяем содержимое файла
    last_line = log_file.read_text().strip().split("\n")[-1]

    assert last_line == "some_func ok"


def test_log_file_error(capsys):
    log_file = Path(BASE_DIRECTORY) / "test.log"

    @log(filepath=str(log_file))
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(5, 0)

    # В консоль ничего не должно попасть
    captured = capsys.readouterr()
    assert captured.out == ""

    # Проверяем содержимое файла
    last_line = log_file.read_text().strip().split("\n")[-1]

    assert last_line == "divide error: ZeroDivisionError. Inputs: (5, 0), {}"


def test_log_file_multiple_calls():
    """Все вызовы дописываются в один файл."""
    log_file_path = Path(BASE_DIRECTORY) / "test.log"

    @log(filepath=str(log_file_path))
    def some_func():
        return "some func result"

    @log(filepath=str(log_file_path))
    def divide(a, b):
        return a / b

    some_func()
    try:
        divide(5, 0)
    except ZeroDivisionError:
        pass
    some_func()

    lines = log_file_path.read_text().strip().split("\n")

    assert lines[-3] == "some_func ok"
    assert lines[-2] == "divide error: ZeroDivisionError. Inputs: (5, 0), {}"
    assert lines[-1] == "some_func ok"


def test_metadata_saved():
    @log()
    def some_func():
        """Описание некой функции"""
        return "some func result"

    assert some_func.__name__ == "some_func"
    assert some_func.__doc__ == "Описание некой функции"
    assert some_func() == "some func result"
