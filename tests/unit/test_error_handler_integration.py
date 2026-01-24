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
    """Мок конфигурации с настройками Telegram"""
    config = Mock(spec=Config)
    config.TELEGRAM_BOT_TOKEN = "6209761567:AAG3QwLjuGqAoFVww4PqvmEcB-O-8qiXZFk"
    config.TELEGRAM_CHAT_ID = "1353223764"
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
@patch('src.error_handler.TelegramNotifier')
def test_error_handler_initialization_with_telegram(mock_notifier_class, mock_config, mock_logger):
    """Тест инициализации ErrorHandler с Telegram уведомлениями"""
    # Мокаем экземпляр TelegramNotifier
    mock_notifier_instance = Mock()
    mock_notifier_class.return_value = mock_notifier_instance

    # Создаем ErrorHandler
    handler = ErrorHandler(mock_config, mock_logger)

    # Проверяем, что TelegramNotifier был инициализирован
    assert handler.telegram_notifier is not None
    mock_notifier_class.assert_called_once_with(
        bot_token=mock_config.TELEGRAM_BOT_TOKEN,
        chat_id=mock_config.TELEGRAM_CHAT_ID,
        logger=mock_logger
    )

    # Проверяем, что был вызван метод start_polling
    mock_notifier_instance.start_polling.assert_called_once()


@pytest.mark.asyncio
@patch('src.error_handler.TelegramNotifier')
async def test_error_handler_send_startup_notification(mock_notifier_class, mock_config, mock_logger):
    """Тест отправки уведомления о запуске"""
    # Мокаем экземпляр TelegramNotifier
    mock_notifier_instance = Mock()
    mock_notifier_class.return_value = mock_notifier_instance

    # Создаем ErrorHandler
    handler = ErrorHandler(mock_config, mock_logger)

    # Асинхронно вызываем метод отправки уведомления о запуске
    await handler.send_startup_notification()

    # Проверяем, что метод был вызван у notifier
    mock_notifier_instance.send_startup_notification.assert_called_once()


@pytest.mark.asyncio
@patch('src.error_handler.TelegramNotifier')
async def test_error_handler_send_shutdown_notification(mock_notifier_class, mock_config, mock_logger):
    """Тест отправки уведомления о завершении"""
    # Мокаем экземпляр TelegramNotifier
    mock_notifier_instance = Mock()
    mock_notifier_class.return_value = mock_notifier_instance

    # Создаем ErrorHandler
    handler = ErrorHandler(mock_config, mock_logger)

    # Асинхронно вызываем метод отправки уведомления о завершении
    await handler.send_shutdown_notification(success_count=5, error_count=1)

    # Проверяем, что метод был вызван у notifier с правильными параметрами
    mock_notifier_instance.send_shutdown_notification.assert_called_once_with(5, 1)


@pytest.mark.asyncio
@patch('src.error_handler.TelegramNotifier')
def test_error_handler_cleanup(mock_notifier_class, mock_config, mock_logger):
    """Тест очистки ресурсов ErrorHandler"""
    # Мокаем экземпляр TelegramNotifier
    mock_notifier_instance = Mock()
    mock_notifier_class.return_value = mock_notifier_instance

    # Создаем ErrorHandler
    handler = ErrorHandler(mock_config, mock_logger)

    # Вызываем метод очистки
    handler.cleanup()

    # Проверяем, что метод stop_polling был вызван у notifier
    mock_notifier_instance.stop_polling.assert_called_once()