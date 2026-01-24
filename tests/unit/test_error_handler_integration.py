"""
Тесты для интеграции TelegramNotifier с ErrorHandler
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Добавляем путь к src для импорта модулей
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.error_handler import ErrorHandler
from src.config import Config


@pytest.fixture
def mock_config():
    """Мок конфигурации без настроек Telegram"""
    config = Mock(spec=Config)
    config.TELEGRAM_BOT_TOKEN = None  # Устанавливаем в None, чтобы не создавался TelegramNotifier
    config.TELEGRAM_CHAT_ID = None  # Устанавливаем в None, чтобы не создавался TelegramNotifier
    config.HH_LOGIN = "test@example.com"
    config.HH_PASSWORD = "password123"
    return config


@pytest.fixture
def mock_logger():
    """Мок логгера"""
    logger = Mock()
    logger.info = Mock()
    logger.error = Mock()
    logger.debug = Mock()
    return logger


@pytest.mark.asyncio
def test_error_handler_initialization_without_telegram(mock_config, mock_logger):
    """Тест инициализации ErrorHandler без Telegram уведомлений"""
    # Создаем ErrorHandler
    handler = ErrorHandler(mock_config, mock_logger)

    # Проверяем, что TelegramNotifier не был инициализирован, потому что TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID равны None
    assert handler.telegram_notifier is None


@pytest.mark.asyncio
async def test_error_handler_send_startup_notification_without_telegram(mock_config, mock_logger):
    """Тест отправки уведомления о запуске без Telegram уведомлений"""
    # Создаем ErrorHandler
    handler = ErrorHandler(mock_config, mock_logger)

    # Асинхронно вызываем метод отправки уведомления о запуске
    # Поскольку telegram_notifier равен None, метод должен завершиться без ошибок
    await handler.send_startup_notification()

    # Проверяем, что telegram_notifier равен None
    assert handler.telegram_notifier is None


@pytest.mark.asyncio
async def test_error_handler_send_shutdown_notification_without_telegram(mock_config, mock_logger):
    """Тест отправки уведомления о завершении без Telegram уведомлений"""
    # Создаем ErrorHandler
    handler = ErrorHandler(mock_config, mock_logger)

    # Асинхронно вызываем метод отправки уведомления о завершении
    # Поскольку telegram_notifier равен None, метод должен завершиться без ошибок
    await handler.send_shutdown_notification(success_count=5, error_count=1)

    # Проверяем, что telegram_notifier равен None
    assert handler.telegram_notifier is None


@pytest.mark.asyncio
def test_error_handler_cleanup_without_telegram(mock_config, mock_logger):
    """Тест очистки ресурсов ErrorHandler без Telegram уведомлений"""
    # Создаем ErrorHandler
    handler = ErrorHandler(mock_config, mock_logger)

    # Вызываем метод очистки
    # Поскольку telegram_notifier равен None, метод должен завершиться без ошибок
    handler.cleanup()

    # Проверяем, что telegram_notifier равен None
    assert handler.telegram_notifier is None