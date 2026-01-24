"""
Модуль логирования
"""
import sys
from loguru import logger as loguru_logger
import logging
from typing import Any


def setup_logger(name: str = __name__, level: str = "INFO"):
    """
    Настройка логгера с форматированием

    :param name: Имя логгера (не используется в loguru, но сохраняем для совместимости)
    :param level: Уровень логирования
    :return: Настроенный объект логгера
    """
    # Удаляем стандартные обработчики
    loguru_logger.remove()

    # Добавляем новый обработчик с нужным форматом
    loguru_logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        level=level,
        colorize=True
    )

    return loguru_logger


# Экспортируем глобальный логгер loguru для совместимости
logger = loguru_logger