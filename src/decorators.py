"""
Модуль с декораторами для логирования и других вспомогательных функций
"""
import inspect
from functools import wraps
from typing import Callable, TypeVar, Any, Union, overload
from loguru import logger

R = TypeVar('R')
P = TypeVar('P')


def log_info(func: Union[Callable[..., R], None] = None):
    """
    Декоратор для логирования информации о вызове синхронной функции.

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
        # Проверяем, является ли функция асинхронной
        if inspect.iscoroutinefunction(func_to_decorate):
            raise ValueError(f"Функция {func_to_decorate.__name__} является асинхронной. "
                             f"Используйте декоратор @async_log_info вместо @log_info.")

        @wraps(func_to_decorate)
        def sync_wrapper(*args: Any, **kwargs: Any) -> R:
            method_name = func_to_decorate.__name__
            logger.info(f"{method_name}() < args={args}, kwargs={kwargs}")

            result: R = func_to_decorate(*args, **kwargs)
            logger.info(f"{method_name}() > {result}")

            return result

        return sync_wrapper  # type: ignore

    # Если декоратор вызывается без скобок (например, @log_info)
    if func is not None:
        return decorator(func)

    # Если декоратор вызывается со скобками (например, @log_info())
    return decorator


def async_log_info(func: Union[Callable[..., R], None] = None):
    """
    Декоратор для логирования информации о вызове асинхронной функции.

    Логирует:
    - Имя функции
    - Аргументы, с которыми была вызвана функция
    - Возвращаемое значение

    Может использоваться как:
    @async_log_info
    def my_func(): ...

    или

    @async_log_info()
    def my_func(): ...
    """
    def decorator(func_to_decorate: Callable[..., R]) -> Callable[..., R]:
        # Проверяем, является ли функция асинхронной
        if not inspect.iscoroutinefunction(func_to_decorate):
            raise ValueError(f"Функция {func_to_decorate.__name__} не является асинхронной. "
                             f"Используйте декоратор @log_info вместо @async_log_info.")

        @wraps(func_to_decorate)
        async def async_wrapper(*args: Any, **kwargs: Any) -> R:
            method_name = func_to_decorate.__name__
            logger.info(f"{method_name}() < args={args}, kwargs={kwargs}")

            result: R = await func_to_decorate(*args, **kwargs)
            logger.info(f"{method_name}() > {result}")

            return result

        return async_wrapper  # type: ignore

    # Если декоратор вызывается без скобок (например, @async_log_info)
    if func is not None:
        return decorator(func)

    # Если декоратор вызывается со скобками (например, @async_log_info())
    return decorator