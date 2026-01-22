"""
Модуль логирования
"""
import logging
import sys
from typing import Any


def setup_logger(name: str = __name__, level: int = logging.INFO) -> logging.Logger:
    """
    Настройка логгера с форматированием
    
    :param name: Имя логгера
    :param level: Уровень логирования
    :return: Настроенный объект логгера
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Предотвращаем добавление обработчиков при повторной инициализации
    if logger.handlers:
        return logger

    # Создаем форматтер для логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Создаем обработчик для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    logger.addHandler(console_handler)

    return logger