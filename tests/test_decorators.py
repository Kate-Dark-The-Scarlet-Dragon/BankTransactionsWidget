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
    captured_lines = captured.out.splitlines()

    assert result == "some funct result"
    assert captured_lines[0] == "some_func start"
    assert captured_lines[1] == "some_func end"
    assert captured_lines[2] == "some_func ok"


def test_log_console_error(capsys):
    @log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(5, 0)

    captured = capsys.readouterr()
    captured_lines = captured.out.splitlines()

    assert captured_lines[0] == "divide start"
    assert captured_lines[1] == "divide end"
    assert captured_lines[2] == "divide error: ZeroDivisionError. Inputs: (5, 0), {}"


def test_log_console_with_kwargs(capsys):
    @log()
    def greet_user(name, greeting="Hello"):
        return f"{greeting}, {name}"

    result = greet_user("Kate", greeting="Hi")
    captured = capsys.readouterr()
    captured_lines = captured.out.splitlines()

    assert result == "Hi, Kate"
    assert captured_lines[0] == "greet_user start"
    assert captured_lines[1] == "greet_user end"
    assert captured_lines[2] == "greet_user ok"


def test_log_no_parentheses_console(capsys):
    @log()
    def get_none():
        return None

    get_none()
    captured = capsys.readouterr()
    captured_lines = captured.out.splitlines()

    assert captured_lines[0] == "get_none start"
    assert captured_lines[1] == "get_none end"
    assert captured_lines[2] == "get_none ok"


def test_log_file_success(capsys):
    log_file_path = Path(BASE_DIRECTORY) / "test.log"

    @log(filepath=str(log_file_path))
    def some_func():
        return "some funct result"

    result = some_func()

    assert result == "some funct result"

    # В консоль ничего не должно попасть
    captured = capsys.readouterr()

    assert captured.out == ""

    # Проверяем содержимое файла
    lines = log_file_path.read_text().strip().split("\n")

    assert lines[-3] == "some_func start"
    assert lines[-2] == "some_func end"
    assert lines[-1] == "some_func ok"


def test_log_file_error(capsys):
    log_file_path = Path(BASE_DIRECTORY) / "test.log"

    @log(filepath=str(log_file_path))
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(5, 0)

    # В консоль ничего не должно попасть
    captured = capsys.readouterr()
    assert captured.out == ""

    # Проверяем содержимое файла
    lines = log_file_path.read_text().strip().split("\n")

    assert lines[-3] == "divide start"
    assert lines[-2] == "divide end"
    assert lines[-1] == "divide error: ZeroDivisionError. Inputs: (5, 0), {}"


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

    assert lines[-9] == "some_func start"
    assert lines[-8] == "some_func end"
    assert lines[-7] == "some_func ok"
    assert lines[-6] == "divide start"
    assert lines[-5] == "divide end"
    assert lines[-4] == "divide error: ZeroDivisionError. Inputs: (5, 0), {}"
    assert lines[-3] == "some_func start"
    assert lines[-2] == "some_func end"
    assert lines[-1] == "some_func ok"


def test_metadata_saved():
    @log()
    def some_func():
        """Описание некой функции"""
        return "some func result"

    assert some_func.__name__ == "some_func"
    assert some_func.__doc__ == "Описание некой функции"
    assert some_func() == "some func result"
