"""
Тесты для модуля логирования
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в путь Python
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.logger import setup_logger


class TestLogger:
    """Тесты для функций логирования"""

    def test_setup_logger_creates_correct_logger(self):
        """Тест настройки логгера"""
        # Выполнение
        logger = setup_logger()

        # Проверка
        assert logger is not None
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'debug')
        assert hasattr(logger, 'warning')

    def test_logger_outputs_to_console(self):
        """Тест вывода логов в консоль"""
        # Подготовка
        logger = setup_logger()

        # Для loguru проверим, что логгер может принимать сообщения
        # без выбрасывания исключений
        try:
            logger.info("Test message")
            success = True
        except Exception:
            success = False

        assert success

    def test_logger_handles_different_log_levels(self):
        """Тест обработки разных уровней логирования"""
        # Подготовка
        logger = setup_logger()

        # Проверка, что логгер может обрабатывать разные уровни
        methods_to_test = ['debug', 'info', 'warning', 'error', 'critical']

        for method in methods_to_test:
            assert hasattr(logger, method), f"Логгер должен иметь метод {method}"

            # Проверяем, что метод можно вызвать без ошибок (хотя бы с пустым сообщением)
            log_method = getattr(logger, method)
            try:
                log_method("")
            except Exception:
                assert False, f"Метод {method} должен быть вызываемым"