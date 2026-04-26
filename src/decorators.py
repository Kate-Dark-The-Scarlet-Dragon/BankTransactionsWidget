from functools import wraps
from typing import Any, Callable


def write_log_text(text: str, filepath: str = "") -> None:
    """
    Логирование информации в консоль/файл.
    :param text: Логируемый текст.
    :param filepath: Путь к файлу логирования. Если не указано - логирование производится в консоль.
    """
    if filepath:
        with open(filepath, "a", encoding="utf-8") as text_stream:
            text_stream.write(f"{text}\n")
    else:
        print(text)


def log(filepath: str = "") -> Callable[..., Any]:
    """
    Декоратор для логирования вызовов функции.

    :param filepath: Путь к файлу логирования. Если не указано - логирование производится в консоль.
    При успешном выполнении функции выводится: "<имя_функции> ok".
    При ошибке: "<имя_функции> error: <тип_ошибки>. Inputs: (<args>), {<kwargs>}".
    """

    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                write_log_text(f"{function.__name__} start", filepath)

                result = function(*args, **kwargs)

                write_log_text(f"{function.__name__} end", filepath)
                write_log_text(f"{function.__name__} ok", filepath)

                return result
            except Exception as ex:
                error_type = type(ex).__name__

                inputs = f"{repr(args) if args else '()'}, {repr(kwargs) if kwargs else '{}'}"
                message = f"{function.__name__} error: {error_type}. Inputs: {inputs}"

                write_log_text(f"{function.__name__} end", filepath)
                write_log_text(message, filepath)

                raise  # Пробрасываем исключение дальше

        return wrapper

    return decorator
