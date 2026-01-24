"""
Модуль с декораторами для логирования и других вспомогательных функций
"""
from functools import wraps
from typing import Callable, TypeVar, Any, Union, overload
from loguru import logger

R = TypeVar('R')
P = TypeVar('P')


def log_info(func: Union[Callable[..., R], None] = None):
    """
    Декоратор для логирования информации о вызове функции.

    Логирует:
    - Имя функции
    - Аргументы, с которыми была вызвана функция
    - Возвращаемое значение

    Может использоваться как:
    @log_info
    def my_func(): ...

    или

    @log_info()
    def my_func(): ...
    """
    def decorator(func_to_decorate: Callable[..., R]) -> Callable[..., R]:
        @wraps(func_to_decorate)
        def wrapper(*args: Any, **kwargs: Any) -> R:
            method_name = func_to_decorate.__name__
            logger.info(f"{method_name}() < args={args}, kwargs={kwargs}")
            result: R = func_to_decorate(*args, **kwargs)
            logger.info(f"{method_name}() > {result}")
            return result

        return wrapper

    # Если декоратор вызывается без скобок (например, @log_info)
    if func is not None:
        return decorator(func)

    # Если декоратор вызывается со скобками (например, @log_info())
    return decorator